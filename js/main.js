'use strict';

/**
 * lights, camera, action!
 */
(function() {

    var $ = function(s) {
        var x = document.querySelectorAll(s);
        return [].slice.call(x, 0);
    };

    function addClass(el, cls) {
        var classes = el.className.split(' ');
        if ( classes.indexOf(cls) == -1 ) classes.push(cls);
        el.className = classes.join(' ');
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
            var _cut = function() {
                var nextChar = dialogues.shift();
                if ( nextChar === undefined ) return; 
                stage.innerHTML += nextChar;
                setTimeout(function() {
                    _cut()
                }, nextEpisode);
            }
            setTimeout(_cut, nextEpisode)
        }, nextSeason)
        info.timeOffset += scene.delay + scene.duration;
        return info
    }, { timeOffset: preShowCommercial })

    ticketCounter.addEventListener('click', function() {
        document.querySelector('.overlay').style.display = 'table';
        var left = document.querySelector('.overlay-left'); 
        var right = document.querySelector('.overlay-right'); 
        addClass(left, 'open');
        addClass(right, 'open');

        /**
         * XXX: time this correctly
         *
         * alternatively, find a way to obtain the necessary value
         * for delay from the stylesheets programmatically.
         */
        setTimeout(function() {
            document.querySelector('body')
               .removeChild(document.querySelector('.preview'));    
            document.querySelector('.main').style.display = 'block';
        }, 800);
        setTimeout(function() {
            document.querySelector('body')
               .removeChild(document.querySelector('.overlay'));    
            addClass(document.querySelector('body'), 'open');
        }, 1600);
    })

    $('.nav').forEach(function(nav) {
        nav.addEventListener('click', function(e) {
            e.preventDefault();
            $('.nav').forEach(function(el) { removeClass(el, 'active') });
            addClass(e.target, 'active');
            var content = document.querySelector('.content');
            removeClass(content, 'fade-toggle');
            addClass(content, 'fade-toggle');
            /**
             * XXX: again, time these values correctly.
             */
            setTimeout(function() {
                $('.content > *').forEach(function(el) { el.className = ''; });
                addClass(document.querySelector(e.target.dataset.target), 'active');
            }, 500);
            setTimeout(function() {
                removeClass(content, 'fade-toggle');
            }, 1000);
        });
    });

    // activate the first nav item
    document.querySelector('.nav').click();

})();
