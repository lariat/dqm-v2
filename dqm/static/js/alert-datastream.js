var visualAlertDataStreamTimeout;

function visualAlertDataStream() {
    if ($ALERT$DATASTREAM) {
        $('body').effect('highlight', {color: '#c12e2a'}, 1000)
        visualAlertDataStreamTimeout = setTimeout(visualAlertDataStream, 1000);
    }
}

function audioAlertDataStream() {
    if ($ALERT$DATASTREAM) {
        $('#alarm-datastream').get(0).play();
    }
}

function alertPanelDataStream(message) {
    if ($ALERT$DATASTREAM) {
        $('#alert-panel-datastream').removeClass('collapse');
        $('#alert-message-datastream').text(message);
    }
}

function alertPanelCollapseDataStream() {
    $('#alert-panel-datastream').addClass('collapse');
}
