'use strict';

/**
 * lights, camera, action!
 */
(function() {
    var script = [{
        text: "Awesomeness",
        delay: 1,
        duration: 0.7
    }, {
        text: ", coming soon to a computer near you",
        delay: 1.5,
        duration: 1.5
    }];
    var preShowCommercial = 1;

    var stage = document.querySelector('.js-message');

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
})();
