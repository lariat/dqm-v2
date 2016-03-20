var alertTimeout;

function visualAlert() {
    if ($ALERT) {
        //$('body').effect('highlight', {color: 'red'}, 1000)
        //$('body').effect('highlight', {color: '#d9534f'}, 1000)
        $('body').effect('highlight', {color: '#c12e2a'}, 1000)
        //$('body').effect('highlight', {color: '#f89406'}, 1000)
        alertTimeout = setTimeout(visualAlert, 1000);
    }
}

function audioAlert() {
    if ($ALERT) {
        $('#alarm').get(0).play();
    }
}

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
