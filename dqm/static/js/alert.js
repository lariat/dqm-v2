var alertTimeout;

var sounds = [
    '/static/sound/ogg/industrial_alarm.ogg',
    '/static/sound/ogg/r2d2.ogg',
    ];

function visualAlert_(elements, loop=false) {
    if ($ALERT) {
        //$(elements).effect('highlight', {color: '#d9534f'}, 1000)
        $(elements).effect('highlight', {color: '#c12e2a'}, 1000)
        if (loop) {
            alertTimeout = setTimeout(visualAlert_.bind(null, elements, loop), 1000);
        }
    }
}

function visualAlert() {
    if ($ALERT) {
        //$('body').effect('highlight', {color: 'red'}, 1000)
        //$('body').effect('highlight', {color: '#d9534f'}, 1000)
        $('body').effect('highlight', {color: '#c12e2a'}, 1000)
        //$('body').effect('highlight', {color: '#f89406'}, 1000)
        alertTimeout = setTimeout(visualAlert, 1000);
    }
}

//function audioAlert() {
//    if ($ALERT) {
//        $('#alarm').get(0).play();
//    }
//}

function audioAlert() {
    if ($ALERT) {
        var sound = sounds[Math.floor(Math.random() * sounds.length)];
        var audio = new Audio(sound);
        audio.play();
    }
}

function alertPanel(message) {
    if ($ALERT) {
        $('#alert-panel').removeClass('collapse');
        $('#alert-message').text(message);
    }
}

function alertPanelCollapse() {
    $('#alert-panel').addClass('collapse');
}

//function alertPanelCollapse() {
//    $('#alert-panel').addClass('collapse');
//    $('#acknowledge').addClass('btn-danger').removeClass('btn-success').text('Acknowledge');
//}

//$('#acknowledge').click(function() {
//    if (!$ACKNOWLEDGED) {
//        $ACKNOWLEDGED = true;
//        $('#acknowledge').addClass('btn-success').removeClass('btn-danger').text('Acknowledged');
//    }
//});

//function toggleAcknowledged(acknowledged) {
//    $('#acknowledge').click(function() {
//        if (!acknowledged) {
//            acknowledged = true;
//            $('#acknowledge').addClass('btn-success').removeClass('btn-danger').text('Acknowledged');
//        }
//    });
//}

//function visualAlert() {
//    $('body').effect('highlight', {color: '#c12e2a'}, 1000)
//    alertTimeout = setTimeout(visualAlert, 1000);
//}

//function audioAlert() {
//    $('#alarm').get(0).play();
//}

//function toggleAlertOn() {
//    $ALERT = true;
//    toggleAlertPanel();
//    audioAlert();
//    setTimeout(function() {
//        if ($ALERT) {
//            console.log("Hello!");
//            visualAlert();
//        }
//    }, 1000);
//}

//function toggleAlertOff() {
//    $ALERT = false;
//}
