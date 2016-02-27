function chart(config) {

    var seriesNames = [ "good", "bad" ],
        //numSamples = 64,
        numSamples = config.stop - config.start;
        stack = d3.layout.stack().values(function (d) { return d.values; });

    var margin = {top: 20, right: 20, bottom: 35, left: 60},
        width = 550 - margin.left - margin.right,
        height = 200 - margin.top - margin.bottom,
        animationDuration = 400,
        delayBetweenBarAnimation = 10,
        numTicks = 8,
        tooltipBottomMargin = 12;

    var binsScale = d3.scale.ordinal()
        //.domain(d3.range(numSamples))
        .domain(d3.range(config.start, config.stop))
        .rangeBands([0, width], 0, 0);

    var xScale = d3.scale.linear()
        //.domain([0, numSamples])
        .domain([config.start, config.stop])
        .range([0, width]);

    var yScale = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(yScale)
        .ticks(numTicks)
        .orient("left");

    var seriesClass = function (seriesName) { return seriesName.toLowerCase(); };
    var layerClass = function (d) { return "layer series-" + seriesClass(d.name); };
    var barDelay = function (d, i) { return i * delayBetweenBarAnimation; };
    var joinKey = function (d) { return d.name; };
    var stackedBarX = function (d) { return binsScale(d.x); };
    var stackedBarY = function (d) { return yScale(d.y0 + d.y); };
    var stackedBarBaseY = function (d) { return yScale(d.y0); };
    var stackedBarWidth = binsScale.rangeBand();
    var stackedBarHeight = function (d) { return yScale(d.y0) - yScale(d.y0 + d.y); };

    var animateStackedBars = function (selection) {
        selection.transition()
            .duration(animationDuration)
            .delay(barDelay)
            .attr("y", stackedBarY)
            .attr("height", stackedBarHeight);
    }

    var svg = d3.select(config.selection)
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    var mainContainer = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var gridContainer = mainContainer.append("g")
        .attr("class", "grid-lines-container");

    // initialize tooltips for bars
    var tooltip = d3.tip()
        .attr("class", "d3-tip")
        .offset([-10, 0])
        .html(function(d) {
            return "Entries: " + d.y + " <br>" + config.x_label +  ": " + d.x;
        })
    mainContainer.call(tooltip);

    // add title
    mainContainer.append("text")
        .attr("x", width)
        .attr("y", -5)
        .attr("text-anchor", "end")
        .style("font-size", "12px")
        .style("font-weight", "bold")
        .text(config.title);

    d3.json(config.json_url + "&query=" + config.good_hits + "+" + config.bad_hits, function(json) {

      var data = [
          {
              name: "good",
              values: _.zip(json[config.good_hits].bins.slice(config.start, config.stop),
                            json[config.good_hits].counts.slice(config.start, config.stop))
                .map(function(pair) {
                  return _.object(["x", "y"], pair);
              })
          },
          {
              name: "bad",
              values: _.zip(json[config.bad_hits].bins.slice(config.start, config.stop),
                            json[config.bad_hits].counts.slice(config.start, config.stop))
                .map(function(pair) {
                  return _.object(["x", "y"], pair);
              })
          }
      ];

      // stack data
      //var data = json.data;
      stack(data);

      // set y-axis range
      var maxStackY = d3.max(data, function (series) { return d3.max(series.values, function (d) { return d.y0 + d.y; }); });
      yScale.domain([0, maxStackY])

      /////////////////////////////////////////////////////////////////////////
      // add bars
      /////////////////////////////////////////////////////////////////////////
      var layers = mainContainer.selectAll(".layer").data(data);

      layers.enter().append("g")
              .attr("class", layerClass);

      layers.selectAll("rect").data(function (d) { return d.values; })
          .enter().append("rect")
              .attr("x", stackedBarX)
              .attr("y", height)
              .attr("width", stackedBarWidth)
              .attr("height", 0)
              .on('mouseover', tooltip.show)
              .on('mouseout', tooltip.hide)
              .call(animateStackedBars);

      /////////////////////////////////////////////////////////////////////////
      // add grid lines
      /////////////////////////////////////////////////////////////////////////
      gridContainer.selectAll(".grid-line").data(yScale.ticks(numTicks))
              .enter().append("line")
                  .attr("class", "grid-line")
                  .attr("x1", 0)
                  .attr("x2", width)
                  .attr("y1", yScale)
                  .attr("y2", yScale);

      /////////////////////////////////////////////////////////////////////////
      // add x-axis and y-axis
      /////////////////////////////////////////////////////////////////////////
      mainContainer.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis)
        .append("text")
          .attr("class", "label")
          .attr("x", width)
          .attr("y", 30)
          .attr("text-anchor", "end")
          .style("font-size", "11px")
          .text(config.x_label);

      mainContainer.append("g")
          .attr("class", "y axis")
          .call(yAxis)
        .append("text")
          .attr("class", "label")
          .attr("y", -50)
          .attr("dy", ".71em")
          .attr("text-anchor", "end")
          .attr("transform", "rotate(-90)")
          .style("font-size", "11px")
          .text("Entries per " + config.x_label);

    })

    function update() {

        d3.json(config.json_url + "&query=" + config.good_hits + "+" + config.bad_hits, function(json) {

            var data = [
                {
                    name: "good",
                    values: _.zip(json[config.good_hits].bins.slice(config.start, config.stop),
                                  json[config.good_hits].counts.slice(config.start, config.stop))
                      .map(function(pair) {
                        return _.object(["x", "y"], pair);
                    })
                },
                {
                    name: "bad",
                    values: _.zip(json[config.bad_hits].bins.slice(config.start, config.stop),
                                  json[config.bad_hits].counts.slice(config.start, config.stop))
                      .map(function(pair) {
                        return _.object(["x", "y"], pair);
                    })
                }
            ];

            //var data = json.data;
            stack(data);

            /////////////////////////////////////////////////////////////////////////
            // update y-axis
            /////////////////////////////////////////////////////////////////////////
            var maxStackY = d3.max(data, function (series) { return d3.max(series.values, function (d) { return d.y0 + d.y; }); });
            yScale.domain([0, maxStackY])

            mainContainer.select(".y.axis")
                .transition()
                .duration(1000)
                .ease("linear")
                .call(yAxis);

            /////////////////////////////////////////////////////////////////////////
            // update grid lines
            /////////////////////////////////////////////////////////////////////////
            var gridSelection = gridContainer.selectAll(".grid-line").data(yScale.ticks(numTicks));

            gridSelection.enter()
                .append("line")
                  .attr("class", "grid-line")
                  .attr("x1", 0)
                  .attr("x2", width)
                  .attr("y1", yScale)
                  .attr("y2", yScale);

            gridSelection.exit().remove();

            gridContainer.selectAll(".grid-line")
                .transition()
                .duration(1000)
                .ease("linear")
                .attr("x1", 0)
                .attr("x2", width)
                .attr("y1", yScale)
                .attr("y2", yScale);

            /////////////////////////////////////////////////////////////////////////
            // update bars
            /////////////////////////////////////////////////////////////////////////
            var groups = mainContainer.selectAll(".layer").data(data);

            groups.enter().append("g")
                    .attr("class", layerClass);

            var rect = groups.selectAll("rect").data(function (d) { return d.values; });

            rect.enter().append("rect")
                .attr("x", stackedBarX)
                .attr("width", stackedBarWidth);

            rect.transition().duration(1000)
                    .ease("linear")
                .attr("y", stackedBarY)
                .attr("height", stackedBarHeight);

            rect.exit()
                .transition().duration(1000)
                    .ease("circle")
                .attr("x", width)
                .remove();

            groups.exit()
                .transition().duration(1000)
                    .ease("circle")
                .attr("x", width)
                .remove();

        })

    }

    var timeout;
    function loadNext() {
        if ($UPDATE) {
            console.log("Updating plots...");
            update();
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

}
