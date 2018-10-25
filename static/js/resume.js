'use strict';

(function() {
    
    Scramble.setConfigGlobal({
        flip: { min: 3, max: 8 },
        interval: { min: 150, max: 190 }
    });
    var target = Scramble.select('.scramble-animate');
    var update = function() { target = target.descramble(); };
    setInterval(update, 3000);
})();
