$( document ).ready(function() {
    var start = 0,
        stop = 64;

    var json_url = $SCRIPT_ROOT + "/histograms?run=" + $RUN + "&subrun=" + $SUBRUN;

    var mwpc_tdc_01_histogram = chart({
        selection: "#mwpc-tdc-01-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_1_good_hits_channel",
        bad_hits: "mwc_tdc_1_bad_hits_channel",
        title: "TDC 01",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_02_histogram = chart({
        selection: "#mwpc-tdc-02-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_2_good_hits_channel",
        bad_hits: "mwc_tdc_2_bad_hits_channel",
        title: "TDC 02",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_03_histogram = chart({
        selection: "#mwpc-tdc-03-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_3_good_hits_channel",
        bad_hits: "mwc_tdc_3_bad_hits_channel",
        title: "TDC 03",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_03_histogram = chart({
        selection: "#mwpc-tdc-04-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_4_good_hits_channel",
        bad_hits: "mwc_tdc_4_bad_hits_channel",
        title: "TDC 04",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_05_histogram = chart({
        selection: "#mwpc-tdc-05-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_5_good_hits_channel",
        bad_hits: "mwc_tdc_5_bad_hits_channel",
        title: "TDC 05",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_06_histogram = chart({
        selection: "#mwpc-tdc-06-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_6_good_hits_channel",
        bad_hits: "mwc_tdc_6_bad_hits_channel",
        title: "TDC 06",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_07_histogram = chart({
        selection: "#mwpc-tdc-07-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_7_good_hits_channel",
        bad_hits: "mwc_tdc_7_bad_hits_channel",
        title: "TDC 07",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_08_histogram = chart({
        selection: "#mwpc-tdc-08-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_8_good_hits_channel",
        bad_hits: "mwc_tdc_8_bad_hits_channel",
        title: "TDC 08",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_09_histogram = chart({
        selection: "#mwpc-tdc-09-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_9_good_hits_channel",
        bad_hits: "mwc_tdc_9_bad_hits_channel",
        title: "TDC 09",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_10_histogram = chart({
        selection: "#mwpc-tdc-10-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_10_good_hits_channel",
        bad_hits: "mwc_tdc_10_bad_hits_channel",
        title: "TDC 10",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_11_histogram = chart({
        selection: "#mwpc-tdc-11-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_11_good_hits_channel",
        bad_hits: "mwc_tdc_11_bad_hits_channel",
        title: "TDC 11",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_12_histogram = chart({
        selection: "#mwpc-tdc-12-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_12_good_hits_channel",
        bad_hits: "mwc_tdc_12_bad_hits_channel",
        title: "TDC 12",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_13_histogram = chart({
        selection: "#mwpc-tdc-13-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_13_good_hits_channel",
        bad_hits: "mwc_tdc_13_bad_hits_channel",
        title: "TDC 13",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_14_histogram = chart({
        selection: "#mwpc-tdc-14-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_14_good_hits_channel",
        bad_hits: "mwc_tdc_14_bad_hits_channel",
        title: "TDC 14",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_15_histogram = chart({
        selection: "#mwpc-tdc-15-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_15_good_hits_channel",
        bad_hits: "mwc_tdc_15_bad_hits_channel",
        title: "TDC 15",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

    var mwpc_tdc_16_histogram = chart({
        selection: "#mwpc-tdc-16-histogram",
        json_url: json_url,
        good_hits: "mwc_tdc_16_good_hits_channel",
        bad_hits: "mwc_tdc_16_bad_hits_channel",
        title: "TDC 16",
        x_label: "TDC channel",
        start: start,
        stop: stop
    });

});
