$( document ).ready(function() {

    var mean_json_url = $SCRIPT_ROOT + "/json?query=tpc_pedestal_mean&run=" + $RUN + "&subrun=" + $SUBRUN;

    var tpc_pedestal_mean_induction = heatmap({
        selection: "#tpc-pedestal-mean-induction",
        json_url: mean_json_url,
        parameter: "tpc_pedestal_mean",
        title: "Pedestal mean on induction plane",
        //legend_title: "Pedestal mean",
        start: 0,
        stop: 240
    });

    var tpc_pedestal_mean_collection = heatmap({
        selection: "#tpc-pedestal-mean-collection",
        json_url: mean_json_url,
        parameter: "tpc_pedestal_mean",
        title: "Pedestal mean on collection plane",
        //legend_title: "Pedestal mean",
        start: 240,
        stop: 480
    });

    var rms_json_url = $SCRIPT_ROOT + "/json?query=tpc_pedestal_rms&run=" + $RUN + "&subrun=" + $SUBRUN;

    var tpc_pedestal_rms_induction = heatmap({
        selection: "#tpc-pedestal-rms-induction",
        json_url: rms_json_url,
        parameter: "tpc_pedestal_rms",
        title: "Pedestal RMS on induction plane",
        //legend_title: "Pedestal RMS",
        start: 0,
        stop: 240
    });

    var tpc_pedestal_rms_collection = heatmap({
        selection: "#tpc-pedestal-rms-collection",
        json_url: rms_json_url,
        parameter: "tpc_pedestal_rms",
        title: "Pedestal RMS on collection plane",
        //legend_title: "Pedestal RMS",
        start: 240,
        stop: 480
    });

    var deviation_json_url = $SCRIPT_ROOT + "/json/tpc-pedestal-deviation?run=" + $RUN + "&subrun=" + $SUBRUN;

    var tpc_pedestal_deviation_induction = heatmap({
        selection: "#tpc-pedestal-deviation-induction",
        json_url: deviation_json_url,
        parameter: "tpc_pedestal_deviation",
        title: "Pedestal deviation on induction plane",
        //legend_title: "Pedestal RMS",
        start: 0,
        stop: 240
    });

    var tpc_pedestal_deviation_collection = heatmap({
        selection: "#tpc-pedestal-deviation-collection",
        json_url: deviation_json_url,
        parameter: "tpc_pedestal_deviation",
        title: "Pedestal deviation on collection plane",
        //legend_title: "Pedestal RMS",
        start: 240,
        stop: 480
    });

});
