(function() {

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
                                                + '&subrun=latest',
        function (data) {
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

            if (data.caen_board_0_data_blocks < 1) {
                $("#caen-board-0").addClass('danger');
            } else {
                $("#caen-board-0").removeClass('danger');
            }

            if (data.caen_board_1_data_blocks < 1) {
                $("#caen-board-1").addClass('danger');
            } else {
                $("#caen-board-1").removeClass('danger');
            }

            if (data.caen_board_2_data_blocks < 1) {
                $("#caen-board-2").addClass('danger');
            } else {
                $("#caen-board-2").removeClass('danger');
            }

            if (data.caen_board_3_data_blocks < 1) {
                $("#caen-board-3").addClass('danger');
            } else {
                $("#caen-board-3").removeClass('danger');
            }

            if (data.caen_board_4_data_blocks < 1) {
                $("#caen-board-4").addClass('danger');
            } else {
                $("#caen-board-4").removeClass('danger');
            }

            if (data.caen_board_5_data_blocks < 1) {
                $("#caen-board-5").addClass('danger');
            } else {
                $("#caen-board-5").removeClass('danger');
            }

            if (data.caen_board_6_data_blocks < 1) {
                $("#caen-board-6").addClass('danger');
            } else {
                $("#caen-board-6").removeClass('danger');
            }

            if (data.caen_board_7_data_blocks < 1) {
                $("#caen-board-7").addClass('danger');
            } else {
                $("#caen-board-7").removeClass('danger');
            }

            if (data.caen_board_24_data_blocks < 1) {
                $("#caen-board-24").addClass('danger');
            } else {
                $("#caen-board-24").removeClass('danger');
            }

            if (data.caen_board_8_data_blocks < 1) {
                $("#caen-board-8").addClass('danger');
            } else {
                $("#caen-board-8").removeClass('danger');
            }

            if (data.caen_board_9_data_blocks < 1) {
                $("#caen-board-9").addClass('danger');
            } else {
                $("#caen-board-9").removeClass('danger');
            }

            if (data.mwc_data_blocks < 1) {
                $("#mwc").addClass('danger');
                if ($UPDATE) {
                    $ALERT = true;
                    visualAlert();
                    audioAlert();
                }
            } else {
                $("#mwc").removeClass('danger');
                $ALERT = false;
            }

            //if (data.wut_data_blocks < 1) {
            //    $("#wut").addClass('danger');
            //} else {
            //    $("#wut").removeClass('danger');
            //}

        });
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

