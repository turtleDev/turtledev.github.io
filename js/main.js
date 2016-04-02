'use strict';

/**
 * lights, camera, action!
 */
(function() {

    function addClass(el, cls) {
        if ( el.className.indexOf(cls) == -1 ) {
            el.className += " " + cls;
        }
    }
    
    function removeClass(el, cls) {
        el.className = el.className.replace(" " +cls, "");
    }

    var director = "turtleDev";
    var chair = document.querySelector('.the-dude');

    scramble.createEmpty(chair, director.length);
    scramble.setText(chair, director);
    setTimeout(function() {
        scramble.descramble(chair);
    }, 1000);

    var ticket = "info";
    var ticketCounter = document.querySelector('.info a');

    setTimeout(function() {
        scramble.createEmpty(ticketCounter, ticket.length);
        scramble.setText(ticketCounter, ticket);
        scramble.descramble(ticketCounter);
    }, 8000);

    ticketCounter.addEventListener("mouseenter", function(e) {
        scramble.enscramble(e.target);
    });

    ticketCounter.addEventListener("mouseleave", function(e) {
        scramble.descramble(e.target);
    });

    var script = [{
        text: "Awesomeness",
        delay: 3,
        duration: 0.7
    }, {
        text: ", coming soon to a computer near you",
        delay: 1.5,
        duration: 1.2
    }];

    var preShowCommercial = 1;

    var stage = document.querySelector('.message');

    script.reduce(function(info, scene) {
        var dialogues = scene.text.split('');
        var nextEpisode = ( scene.duration / dialogues.length ) * 1000;
        var nextSeason = (info.timeOffset + scene.delay) * 1000;
        setTimeout(function() {
            var cut = setInterval(function() {
                var nextChar = dialogues.shift();
                if ( nextChar === undefined ) {
                    clearInterval(cut);
                    return;
                }
                stage.innerHTML += nextChar;
            }, nextEpisode)
        }, nextSeason)
        info.timeOffset += scene.delay + scene.duration;
        return info
    }, { timeOffset: preShowCommercial })

    var newMovie = document.querySelector('.greeting');
    ticketCounter.addEventListener('click', function() {
        newMovie.style.display = 'table';
        removeClass(newMovie, 'hide');
        addClass(newMovie, 'show');
    })

     var closeShow = document.querySelector('.greeting a[href="#"]');
     closeShow.addEventListener('click', function() {
        removeClass(newMovie, 'show');
        addClass(newMovie, 'hide');
 
 	/**
 	 * XXX: make sure the timeout duration is equal to or greater than
         * the CSS transition time
         */
        setTimeout(function() {
            newMovie.style.display = 'none';
        }, 1000);
    })
})();
