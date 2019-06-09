---
title: "Golang Concurrency Patterns: Double Checked Locking"
date: 2019-06-09T02:04:38+05:30
draft: false
---

Golang is quite pecuiliar in the way that it approaches Object Oriented Programming.
Almost all of us are familiar with some OO language that either has classes or plain
objects with a delegation mechanism (I'm looking at you, JavaScript)

And yet it's exhilarating to write OO style code in Golang. I never realised I could do
so much (if not everything) without classes and generics. My code ends up being a lot more
robust and malleable.

As with most other things in Programming, whenever you learn a new language and/or stack, you
tend to bring with you your previous knowledge and preferences. Among these are design patterns,
and in context of this blog post; concurrency patterns. One such pattern is the 
[Check Lock Check](https://en.wikipedia.org/wiki/Double-checked_locking) (aka Double-checked locking) pattern. 

Wikipedia defines Check Lock Check as:

> In software engineering, double-checked locking (also known as "double-checked locking optimization") is a software design pattern used to reduce the overhead of acquiring a lock by testing the locking criterion (the "lock hint") before acquiring the lock. Locking occurs only if the locking criterion check indicates that locking is required.

Here is an example of this pattern (from wiki)
{{< highlight go "linenos=table" >}}
package main
import "sync"

var arrMu sync.Mutex
var arr []int

// getArr retrieves arr, lazily initializing if needed. Double-checked locking
// avoids locking the entire function, and ensures that arr will be
// initialized only once.
func getArr() *[]int {
    if arr != nil { // 1st check
        return &arr 
    }   

    arrMu.Lock()
    defer arrMu.Unlock()

    if arr != nil { // 2nd check
        return &arr
    }
    arr = []int{0, 1, 2}
    return &arr
}

func main() {
    // thanks to double-checked locking, two goroutines attempting to getArr()
    // will not cause double-initialization
    go getArr()
    go getArr()
}
{{< / highlight >}}

Double checked locking let's you make lazy initialisations idempotent and thread safe. Though
that sounds good on paper, is it really that practical in real applications?

Let's think about what lazy initialisation is used for:

* to defer initialisation of expensive resources until they are actually required (virtual proxy)
* to defer initialisation until certain facts have been determined (factory)

Let's look at an example of a virtual proxy:

{{< highlight go "linenos=table" >}}
package main

import (
	"io"
	"os"
	"sync"
	"time"
)

type virtualFile struct {
	closed bool
	mu     sync.Mutex
	fd     *os.File
	Path   string
}

func (file *virtualFile) Read(p []byte) (n int, err error) {
	if file.fd == nil {
		file.mu.Lock()
		defer file.mu.Unlock()
		if file.fd == nil {
			f, err := os.Open(file.Path)
			if err != nil {
				return 0, err
			}
			file.fd = f
		}
	}
	return file.fd.Read(p)
}

func (file *virtualFile) Close() error {
	if file.closed {
		return nil
	}
	file.mu.Lock()
	defer file.mu.Unlock()
	if file.closed {
		return nil
	}
	err := file.Close()
	file.closed = true
	return err
}

func process(r io.Reader, done func()) {
	defer done()
	// do some other work
	time.Sleep(1 * time.Second)
	buf := make([]byte, 4*1024) // 4kb
	for {
		n, err := r.Read(buf)
		// do stuff
	}
}

func main() {
	f := &virtualFile{Path: "/var/log/byte-stream-log"}
	var wg sync.WaitGroup
	wg.Add(10)
	for i := 0; i < 10; i++ {
		go process(f, wg.Done)
	}
	wg.Wait()
}
{{< / highlight >}}

Here we have a program that reads 4kb chunks from a shared source file and does something with it.
Now this may look like a good idea, except it isn't that great considering what you gain from it.
Startup times are usually not a problem for networked applications (though they maybe an issue, for
short lived services). Use this pattern for lazy initialisation where the gain from delaying the initialisation
is worth the added maintaince cost. In most cases, initialising things at the start of the program should
be more than enough. Use this pattern for lazy initialisations sparingly.

(side note: I'm not sure if reading a file from different goroutines sans synchronisation is a good idea. It works
on Linux/Mac/Windows but I'm not familiar enough with threads and system calls to say this operation is safe. Stay
safe kids, don't rely on magic.)

Moving on to the next use: factories. Well to be exact, factories with caching/pooling. Why the distinction?
Let's look at a typical use pattern for a factory:


{{< highlight go "linenos=table" >}}
package main

import (
	"fmt"
	"net/http"
	"strings"
)

// Service represents an external service
type Service interface {
	Do(action string)
}

// ServiceFactory is a component capable of constructing
// a service interface with a given service name
type ServiceFactory interface {
	New(serviceName string) (Service, error)
}

// stub service implementations
type FooService struct {
	Service
}

type BarService struct {
	Service
}

// default ServiceFactory implementation
type serviceFactory struct {
	// data
}

func (fac *serviceFactory) New(serviceName string) (Service, error) {
	serviceName = strings.TrimSpace(serviceName)
	switch serviceName {
	case "foo":
		return &FooService{ /* service specific config */ }, nil
	case "bar":
		return &BarService{ /* service specific config */ }, nil
	}
	return nil, fmt.Errorf("don't know how to construct %s", serviceName)
}

type serviceHandler struct {
	srvFactory ServiceFactory
}

func (handler *serviceHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {

	// the code below extracts the service name
	// and action name
	pathComponents := strings.Split(r.URL.Path, "/")
	l := len(pathComponents) - 1
	if pathComponents[l] == "/" {
		pathComponents = pathComponents[:l]
		l = len(pathComponents)
	}
	actionName := pathComponents[l]
	srvName := pathComponents[l-1]

	// construct the service from the factory
	// and call the specified action
	srv, err := handler.srvFactory.New(srvName)
	if err != nil {
		w.WriteHeader(http.StatusNotFound)
		return
	}
	srv.Do(actionName)
}

func main() {
	handler := &serviceHandler{
		srvFactory: new(serviceFactory),
	}

	// requests will be of the form
	// /v0/dispatch/<serviceName>/<action>
	http.Handle("/v0/dispatch/", handler)
	http.ListenAndServe(":8080", nil)
}
{{< / highlight >}}

Do you see the problem? A service object will be constructed for each request even though
we only have a few service implementations. Now _this_ can be a valid use case in case
each constructed service _has to be_ constructed for every request, probably involving some
form of request scoping. However what if you wanted to share them? Let's rewrite the service factory
implementation to use double checked locking.


{{< highlight go "linenos=table" >}}
// default ServiceFactory implementation
type serviceFactory struct {
	mu    sync.Mutex
	cache map[string]Service
}

func (fac *serviceFactory) New(serviceName string) (Service, error) {
	// check if the service has already been constructed -- (1)
	serviceName = strings.TrimSpace(serviceName)
	if srv, exists := fac.cache[serviceName]; exists {
		return srv, nil
	}

	fac.mu.Lock()
	defer fac.mu.Unlock()

	// ensure that the service wasn't already created during
	// lock-acquisition by a similar goroutine -- (2)
	if srv, exists := fac.cache[serviceName]; exists {
		return srv, nil
	}

	// construct the service and add it to the cache 
	var newService Service
	switch serviceName {
	case "foo":
		newService = &FooService{ /* service specific config */ }
	case "bar":
		newService = &BarService{ /* service specific config */ }
	}
	if newService == nil {
		return nil, fmt.Errorf("don't know how to construct %s", serviceName)
	}
	fac.cache[serviceName] = newService
	return newService, nil
}
{{< / highlight >}}

There. Much better. This pattern can be applied anywhere where you need to
construct an object lazily and save it for future re-use. Double check locking
ensures that the bare minimum amount of work is done and that there are no
duplicate initialisations.

# Before you go and start (ab)using this pattern

Double checked locking is a fairly advanced design pattern. And though it may
sound really good on paper, I'd advise using against it, _unless_ double initialisation
is as an end of the world event for you, or if you construct and pool thousands or even
millions of such object and the cost of construction is a bottle neck.

Double checked locking tends to end up hurting the readability of your code. Use this pattern
_after_ you know that using it would actually help with security or performance. 

As Donald Knuth said

> premature optimization is the root of all evil

that said, Go and have fun. :)
 