(function() {

    var dataStreamAudioAlert = true;

    var caenBoard0Alert = false,
        caenBoard1Alert = false,
        caenBoard2Alert = false,
        caenBoard3Alert = false,
        caenBoard4Alert = false,
        caenBoard5Alert = false,
        caenBoard6Alert = false,
        caenBoard7Alert = false,
        caenBoard8Alert = false,
        caenBoard9Alert = false,
        caenBoard24Alert = false,
        mwcAlert = false,
        wutAlert = false;

    var caen_board_0_data_blocks_penultimate,
        caen_board_1_data_blocks_penultimate,
        caen_board_2_data_blocks_penultimate,
        caen_board_3_data_blocks_penultimate,
        caen_board_4_data_blocks_penultimate,
        caen_board_5_data_blocks_penultimate,
        caen_board_6_data_blocks_penultimate,
        caen_board_7_data_blocks_penultimate,
        caen_board_24_data_blocks_penultimate,
        caen_board_8_data_blocks_penultimate,
        caen_board_9_data_blocks_penultimate,
        mwc_data_blocks_penultimate,
        wut_data_blocks_penultimate;

    $(document).ready(function() {
        fillTable();
    });

    function fillTable() {
        $.getJSON($SCRIPT_ROOT + '/json?query=' + 'caen_board_0_data_blocks+'
                                                + 'caen_board_1_data_blocks+'
                                                + 'caen_board_2_data_blocks+'
                                                + 'caen_board_3_data_blocks+'
                                                + 'caen_board_4_data_blocks+'
                                                + 'caen_board_5_data_blocks+'
                                                + 'caen_board_6_data_blocks+'
                                                + 'caen_board_7_data_blocks+'
                                                + 'caen_board_8_data_blocks+'
                                                + 'caen_board_9_data_blocks+'
                                                + 'caen_board_24_data_blocks+'
                                                + 'mwc_data_blocks+'
                                                + 'wut_data_blocks'
                                                + '&run=' + $RUN
                                                + '&subrun=' + $SUBRUN,
        function (data) {
            $("#caen-board-0-data-blocks").html(JSON.stringify(data.caen_board_0_data_blocks));
            $("#caen-board-1-data-blocks").html(JSON.stringify(data.caen_board_1_data_blocks));
            $("#caen-board-2-data-blocks").html(JSON.stringify(data.caen_board_2_data_blocks));
            $("#caen-board-3-data-blocks").html(JSON.stringify(data.caen_board_3_data_blocks));
            $("#caen-board-4-data-blocks").html(JSON.stringify(data.caen_board_4_data_blocks));
            $("#caen-board-5-data-blocks").html(JSON.stringify(data.caen_board_5_data_blocks));
            $("#caen-board-6-data-blocks").html(JSON.stringify(data.caen_board_6_data_blocks));
            $("#caen-board-7-data-blocks").html(JSON.stringify(data.caen_board_7_data_blocks));
            $("#caen-board-24-data-blocks").html(JSON.stringify(data.caen_board_24_data_blocks));
            $("#caen-board-9-data-blocks").html(JSON.stringify(data.caen_board_8_data_blocks));
            $("#caen-board-8-data-blocks").html(JSON.stringify(data.caen_board_9_data_blocks));
            $("#mwc-data-blocks").html(JSON.stringify(data.mwc_data_blocks));
            $("#wut-data-blocks").html(JSON.stringify(data.wut_data_blocks));

            if (data.caen_board_0_data_blocks < 1) {
                $("#caen-board-0-data-blocks").addClass('danger');
            } else {
                $("#caen-board-0-data-blocks").removeClass('danger');
            }

            if (data.caen_board_1_data_blocks < 1) {
                $("#caen-board-1-data-blocks").addClass('danger');
            } else {
                $("#caen-board-1-data-blocks").removeClass('danger');
            }

            if (data.caen_board_2_data_blocks < 1) {
                $("#caen-board-2-data-blocks").addClass('danger');
            } else {
                $("#caen-board-2-data-blocks").removeClass('danger');
            }

            if (data.caen_board_3_data_blocks < 1) {
                $("#caen-board-3-data-blocks").addClass('danger');
            } else {
                $("#caen-board-3-data-blocks").removeClass('danger');
            }

            if (data.caen_board_4_data_blocks < 1) {
                $("#caen-board-4-data-blocks").addClass('danger');
            } else {
                $("#caen-board-4-data-blocks").removeClass('danger');
            }

            if (data.caen_board_5_data_blocks < 1) {
                $("#caen-board-5-data-blocks").addClass('danger');
            } else {
                $("#caen-board-5-data-blocks").removeClass('danger');
            }

            if (data.caen_board_6_data_blocks < 1) {
                $("#caen-board-6-data-blocks").addClass('danger');
            } else {
                $("#caen-board-6-data-blocks").removeClass('danger');
            }

            if (data.caen_board_7_data_blocks < 1) {
                $("#caen-board-7-data-blocks").addClass('danger');
            } else {
                $("#caen-board-7-data-blocks").removeClass('danger');
            }

            if (data.caen_board_24_data_blocks < 1) {
                $("#caen-board-24-data-blocks").addClass('danger');
            } else {
                $("#caen-board-24-data-blocks").removeClass('danger');
            }

            if (data.caen_board_8_data_blocks < 1) {
                $("#caen-board-8-data-blocks").addClass('danger');
            } else {
                $("#caen-board-8-data-blocks").removeClass('danger');
            }

            if (data.caen_board_9_data_blocks < 1) {
                $("#caen-board-9-data-blocks").addClass('danger');
            } else {
                $("#caen-board-9-data-blocks").removeClass('danger');
            }

            if (data.mwc_data_blocks < 1) {
                $("#mwc-data-blocks").addClass('danger');
            } else {
                $("#mwc-data-blocks").removeClass('danger');
            }

            //if (data.wut_data_blocks < 1) {
            //    $("#wut-data-blocks").addClass('danger');
            //} else {
            //    $("#wut-data-blocks").removeClass('danger');
            //}
        });

        $.getJSON($SCRIPT_ROOT + '/json?query=' + 'caen_board_0_data_blocks+'
                                                + 'caen_board_1_data_blocks+'
                                                + 'caen_board_2_data_blocks+'
                                                + 'caen_board_3_data_blocks+'
                                                + 'caen_board_4_data_blocks+'
                                                + 'caen_board_5_data_blocks+'
                                                + 'caen_board_6_data_blocks+'
                                                + 'caen_board_7_data_blocks+'
                                                + 'caen_board_8_data_blocks+'
                                                + 'caen_board_9_data_blocks+'
                                                + 'caen_board_24_data_blocks+'
                                                + 'mwc_data_blocks+'
                                                + 'wut_data_blocks'
                                                + '&run=' + $RUN
                                                + '&subrun=penultimate', updatePenultimateSubRun)
        function updatePenultimateSubRun(data) {

            caen_board_0_data_blocks_penultimate = data.caen_board_0_data_blocks,
            caen_board_1_data_blocks_penultimate = data.caen_board_1_data_blocks,
            caen_board_2_data_blocks_penultimate = data.caen_board_2_data_blocks,
            caen_board_3_data_blocks_penultimate = data.caen_board_3_data_blocks,
            caen_board_4_data_blocks_penultimate = data.caen_board_4_data_blocks,
            caen_board_5_data_blocks_penultimate = data.caen_board_5_data_blocks,
            caen_board_6_data_blocks_penultimate = data.caen_board_6_data_blocks,
            caen_board_7_data_blocks_penultimate = data.caen_board_7_data_blocks,
            caen_board_24_data_blocks_penultimate = data.caen_board_24_data_blocks,
            caen_board_8_data_blocks_penultimate = data.caen_board_8_data_blocks,
            caen_board_9_data_blocks_penultimate = data.caen_board_9_data_blocks,
            mwc_data_blocks_penultimate = data.mwc_data_blocks,
            wut_data_blocks_penultimate = data.wut_data_blocks;

        }

        $.getJSON($SCRIPT_ROOT + '/json?query=' + 'caen_board_0_data_blocks+'
                                                + 'caen_board_1_data_blocks+'
                                                + 'caen_board_2_data_blocks+'
                                                + 'caen_board_3_data_blocks+'
                                                + 'caen_board_4_data_blocks+'
                                                + 'caen_board_5_data_blocks+'
                                                + 'caen_board_6_data_blocks+'
                                                + 'caen_board_7_data_blocks+'
                                                + 'caen_board_8_data_blocks+'
                                                + 'caen_board_9_data_blocks+'
                                                + 'caen_board_24_data_blocks+'
                                                + 'mwc_data_blocks+'
                                                + 'wut_data_blocks'
                                                + '&run=' + $RUN
                                                + '&subrun=latest', updateLatestSubRun)

        function updateLatestSubRun(data) {

            $("#caen-board-0-data-blocks-latest").html(JSON.stringify(data.caen_board_0_data_blocks));
            $("#caen-board-1-data-blocks-latest").html(JSON.stringify(data.caen_board_1_data_blocks));
            $("#caen-board-2-data-blocks-latest").html(JSON.stringify(data.caen_board_2_data_blocks));
            $("#caen-board-3-data-blocks-latest").html(JSON.stringify(data.caen_board_3_data_blocks));
            $("#caen-board-4-data-blocks-latest").html(JSON.stringify(data.caen_board_4_data_blocks));
            $("#caen-board-5-data-blocks-latest").html(JSON.stringify(data.caen_board_5_data_blocks));
            $("#caen-board-6-data-blocks-latest").html(JSON.stringify(data.caen_board_6_data_blocks));
            $("#caen-board-7-data-blocks-latest").html(JSON.stringify(data.caen_board_7_data_blocks));
            $("#caen-board-24-data-blocks-latest").html(JSON.stringify(data.caen_board_24_data_blocks));
            $("#caen-board-9-data-blocks-latest").html(JSON.stringify(data.caen_board_8_data_blocks));
            $("#caen-board-8-data-blocks-latest").html(JSON.stringify(data.caen_board_9_data_blocks));
            $("#mwc-data-blocks-latest").html(JSON.stringify(data.mwc_data_blocks));
            $("#wut-data-blocks-latest").html(JSON.stringify(data.wut_data_blocks));

            if (data.caen_board_0_data_blocks < 1 && caen_board_0_data_blocks_penultimate) {
                $("#caen-board-0").addClass('danger');
                caenBoard0Alert = true;
            } else {
                $("#caen-board-0").removeClass('danger');
                caenBoard0Alert = false;
            }

            if (data.caen_board_1_data_blocks < 1 && caen_board_1_data_blocks_penultimate) {
                $("#caen-board-1").addClass('danger');
                caenBoard1Alert = true;
            } else {
                $("#caen-board-1").removeClass('danger');
                caenBoard1Alert = false;
            }

            if (data.caen_board_2_data_blocks < 1 && caen_board_2_data_blocks_penultimate) {
                $("#caen-board-2").addClass('danger');
                caenBoard2Alert = true;
            } else {
                $("#caen-board-2").removeClass('danger');
                caenBoard2Alert = false;
            }

            if (data.caen_board_3_data_blocks < 1 && caen_board_3_data_blocks_penultimate) {
                $("#caen-board-3").addClass('danger');
                caenBoard3Alert = true;
            } else {
                $("#caen-board-3").removeClass('danger');
                caenBoard3Alert = false;
            }

            if (data.caen_board_4_data_blocks < 1 && caen_board_4_data_blocks_penultimate) {
                $("#caen-board-4").addClass('danger');
                caenBoard4Alert = true;
            } else {
                $("#caen-board-4").removeClass('danger');
                caenBoard4Alert = false;
            }

            if (data.caen_board_5_data_blocks < 1 && caen_board_5_data_blocks_penultimate) {
                $("#caen-board-5").addClass('danger');
                caenBoard5Alert = true;
            } else {
                $("#caen-board-5").removeClass('danger');
                caenBoard5Alert = false;
            }

            if (data.caen_board_6_data_blocks < 1 && caen_board_6_data_blocks_penultimate) {
                $("#caen-board-6").addClass('danger');
                caenBoard6Alert = true;
            } else {
                $("#caen-board-6").removeClass('danger');
                caenBoard6Alert = false;
            }

            if (data.caen_board_7_data_blocks < 1 && caen_board_7_data_blocks_penultimate) {
                $("#caen-board-7").addClass('danger');
                caenBoard7Alert = true;
            } else {
                $("#caen-board-7").removeClass('danger');
                caenBoard7Alert = false;
            }

            if (data.caen_board_24_data_blocks < 1 && caen_board_24_data_blocks_penultimate) {
                $("#caen-board-24").addClass('danger');
                caenBoard24Alert = true;
            } else {
                $("#caen-board-24").removeClass('danger');
                caenBoard24Alert = false;
            }

            if (data.caen_board_8_data_blocks < 1 && caen_board_8_data_blocks_penultimate) {
                $("#caen-board-8").addClass('danger');
                caenBoard8Alert = true;
            } else {
                $("#caen-board-8").removeClass('danger');
                caenBoard8Alert = false;
            }

            if (data.caen_board_9_data_blocks < 1 && caen_board_9_data_blocks_penultimate) {
                $("#caen-board-9").addClass('danger');
                caenBoard9Alert = true;
            } else {
                $("#caen-board-9").removeClass('danger');
                caenBoard9Alert = false;
            }

            if (data.mwc_data_blocks < 1 && mwc_data_blocks_penultimate < 1) {
                $("#mwc").addClass('danger');
                mwcAlert = true;
            } else {
                $("#mwc").removeClass('danger');
                mwcAlert = false;
            }

            //if (data.wut_data_blocks < 1 && wut_data_blocks_penultimate < 1) {
            //    $("#wut").addClass('danger');
            //    wutAlert = true;
            //} else {
            //    $("#wut").removeClass('danger');
            //    wutAlert = false;
            //}

            if ($UPDATE) {
                if (caenBoard0Alert  ||
                    caenBoard1Alert  ||
                    caenBoard2Alert  ||
                    caenBoard3Alert  ||
                    caenBoard4Alert  ||
                    caenBoard5Alert  ||
                    caenBoard6Alert  ||
                    caenBoard7Alert  ||
                    caenBoard8Alert  ||
                    caenBoard9Alert  ||
                    caenBoard24Alert ||
                    mwcAlert         ||
                    wutAlert) {
                    $ALERT = true;
                } else {
                    $ALERT = false;
                }
            }

            if ($ALERT) {
                visualAlert();
                if (dataStreamAudioAlert) {
                    audioAlert();
                    dataStreamAudioAlert = false;
                }
                alertPanel('Missing data blocks!');
            } else {
                dataStreamAudioAlert = true;
                alertPanelCollapse();
            }

        }
    }

    var timeout;
    function loadNext() {
        if ($UPDATE) {
            fillTable();
            timeout = setTimeout(loadNext, 15000);
        }
    }

    setTimeout(function() {
        if ($UPDATE) {
            console.log("Hello!");
            loadNext();
        } else {
            console.log("Goodbye!");
        }
    }, 10000);

}) ();

