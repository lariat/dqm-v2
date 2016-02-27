$( document ).ready(function() {

    // CAEN board 7
    var caen_board_7_pedestal_mean = heatmap({
        selection: "#caen-board-7-pedestal-mean",
        json_url: $SCRIPT_ROOT + "/json?query=caen_board_7_pedestal_mean&run=" + $RUN + "&subrun=" + $SUBRUN,
        parameter: "caen_board_7_pedestal_mean",
        title: "Pedestal mean on CAEN board 7 (V1740B)",
        width: 540,
        height: 290,
        rows: 4,
        cols: 8,
        start: 0,
        stop: 64,
        channel_offset: 0,
        domain: [ 0., 819.2, 1638.4, 2457.6, 3276.8, 4096. ],
        autoscale: true,
    });

    var caen_board_7_pedestal_rms = heatmap({
        selection: "#caen-board-7-pedestal-rms",
        json_url: $SCRIPT_ROOT + "/json?query=caen_board_7_pedestal_rms&run=" + $RUN + "&subrun=" + $SUBRUN,
        parameter: "caen_board_7_pedestal_rms",
        title: "Pedestal RMS on CAEN board 7 (V1740)",
        width: 540,
        height: 290,
        rows: 4,
        cols: 8,
        start: 0,
        stop: 32,
        channel_offset: 32,
        domain: [],
        autoscale: true,
    });

    // CAEN board 8
    var caen_board_8_pedestal_mean = heatmap({
        selection: "#caen-board-8-pedestal-mean",
        json_url: $SCRIPT_ROOT + "/json?query=caen_board_8_pedestal_mean&run=" + $RUN + "&subrun=" + $SUBRUN,
        parameter: "caen_board_8_pedestal_mean",
        title: "Pedestal mean on CAEN board 8 (V1751)",
        width: 540,
        height: 270,
        rows: 2,
        cols: 4,
        start: 0,
        stop: 8,
        channel_offset: 0,
        domain: [ 0., 204.6, 409.2, 613.8, 818.4, 1023. ],
        autoscale: true,
    });

    var caen_board_8_pedestal_rms = heatmap({
        selection: "#caen-board-8-pedestal-rms",
        json_url: $SCRIPT_ROOT + "/json?query=caen_board_8_pedestal_rms&run=" + $RUN + "&subrun=" + $SUBRUN,
        parameter: "caen_board_8_pedestal_rms",
        title: "Pedestal RMS on CAEN board 8 (V1751)",
        width: 540,
        height: 270,
        rows: 2,
        cols: 4,
        start: 0,
        stop: 8,
        channel_offset: 0,
        domain: [],
        autoscale: true,
    });

    // CAEN board 9
    var caen_board_9_pedestal_mean = heatmap({
        selection: "#caen-board-9-pedestal-mean",
        json_url: $SCRIPT_ROOT + "/json?query=caen_board_9_pedestal_mean&run=" + $RUN + "&subrun=" + $SUBRUN,
        parameter: "caen_board_9_pedestal_mean",
        title: "Pedestal mean on CAEN board 9 (V1751)",
        width: 540,
        height: 270,
        rows: 2,
        cols: 4,
        start: 0,
        stop: 8,
        channel_offset: 0,
        domain: [ 0., 204.6, 409.2, 613.8, 818.4, 1023. ],
        autoscale: true,
    });

    var caen_board_9_pedestal_rms = heatmap({
        selection: "#caen-board-9-pedestal-rms",
        json_url: $SCRIPT_ROOT + "/json?query=caen_board_9_pedestal_rms&run=" + $RUN + "&subrun=" + $SUBRUN,
        parameter: "caen_board_9_pedestal_rms",
        title: "Pedestal RMS on CAEN board 9 (V1751)",
        width: 540,
        height: 270,
        rows: 2,
        cols: 4,
        start: 0,
        stop: 8,
        channel_offset: 0,
        domain: [],
        autoscale: true,
    });

    // CAEN board 24
    var caen_board_24_pedestal_mean = heatmap({
        selection: "#caen-board-24-pedestal-mean",
        json_url: $SCRIPT_ROOT + "/json?query=caen_board_24_pedestal_mean&run=" + $RUN + "&subrun=" + $SUBRUN,
        parameter: "caen_board_24_pedestal_mean",
        title: "Pedestal mean on CAEN board 24 (V1740B)",
        width: 540,
        height: 470,
        rows: 8,
        cols: 8,
        start: 0,
        stop: 64,
        channel_offset: 0,
        domain: [ 0., 819.2, 1638.4, 2457.6, 3276.8, 4096. ],
        autoscale: true,
    });

    var caen_board_24_pedestal_rms = heatmap({
        selection: "#caen-board-24-pedestal-rms",
        json_url: $SCRIPT_ROOT + "/json?query=caen_board_24_pedestal_rms&run=" + $RUN + "&subrun=" + $SUBRUN,
        parameter: "caen_board_24_pedestal_rms",
        title: "Pedestal RMS on CAEN board 24 (V1740B)",
        width: 540,
        height: 470,
        rows: 8,
        cols: 8,
        start: 0,
        stop: 64,
        channel_offset: 0,
        domain: [],
        autoscale: true,
    });

});
