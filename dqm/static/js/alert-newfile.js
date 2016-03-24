var visualAlertNewFileTimeout;

function visualAlertNewFile() {
    if ($ALERT$NEWFILE) {
        $('body').effect('highlight', {color: '#c12e2a'}, 1000)
        visualAlertNewFileTimeout = setTimeout(visualAlertNewFile, 1000);
    }
}

function audioAlertNewFile() {
    if ($ALERT$NEWFILE) {
        $('#alarm-newfile').get(0).play();
    }
}

function alertPanelNewFile(message) {
    if ($ALERT$NEWFILE) {
        $('#alert-panel-newfile').removeClass('collapse');
        $('#alert-message-newfile').text(message);
    }
}

function alertPanelCollapseNewFile() {
    $('#alert-panel-newfile').addClass('collapse');
}
