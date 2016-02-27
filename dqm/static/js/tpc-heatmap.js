function heatmap(config) {

    var margin = {top: 60, right: 90, bottom: 30, left: 50},
    //var margin = {top: 20, right: 90, bottom: 30, left: 50},
        width = 540 - margin.left - margin.right,
        height = 440 - margin.top - margin.bottom;

    var x = d3.scale.linear().range([0, width]),
        y = d3.scale.linear().range([height, 0]);

    var color = d3.scale.linear()
                   .domain([0, 1])
                   .range(['#f6faaa', '#fee08b', '#fdae61', '#f46d43', '#d53e4f', '#9e0142']);

    // This could be inferred from the data if it weren't sparse.
    var xStep = 1,
        yStep = 1;

    var rows = +15;
    var cols = +16;

    var svg = d3.select(config.selection).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.json(config.json_url, function(data) {

        var buckets = data[config.parameter].slice(config.start, config.stop).map(function(datum, idx) {
            var x = idx % cols;
            var y = Math.floor(idx / cols);
            return {
                x: x,
                y: y,
                channel: idx,
                value: datum
            }
        });

        x.domain([0, cols]);
        y.domain([0, rows]);
        color.domain(numeric.linspace(d3.min(buckets, function(d) { return d.value; }), d3.max(buckets, function(d) { return d.value; }), 6));

        var tip = d3.tip()
            .attr('class', 'd3-tip')
            .style("visibility","visible")
            .offset([-15, 0])
            .html(function(d) {
                return "Channel: " + d.channel + " <br> Value: <span style='color:darkorange'>" + d.value + "</span>";
            });

        svg.call(tip);

        // Display the tiles for each non-zero bucket.
        // See http://bl.ocks.org/3074470 for an alternative implementation.
        svg.selectAll(".tile")
            .data(buckets)
          .enter().append("rect")
            .attr("class", "tile")
            .attr("x", function(d) { return x(d.x); })
            .attr("y", function(d) { return y(d.y + yStep); })
            .attr("width", x(xStep) - x(0))
            .attr("height",  y(0) - y(yStep))
            .style("fill", function(d) { return color(d.value); })
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide);

        // Add a legend for the color values.
        var legend = svg.selectAll(".legend")
            .data(color.ticks(6).reverse())
          .enter().append("g")
            .attr("class", "legend")
            .attr("transform", function(d, i) { return "translate(" + (width + 20) + "," + (20 + i * 20) + ")"; });

        legend.append("rect")
            .attr("width", 20)
            .attr("height", 20)
            .style("fill", color);

        legend.append("text")
            .attr("x", 26)
            .attr("y", 10)
            .attr("dy", ".35em")
            .text(String);

        svg.append("text")
            .attr("class", "label")
            .attr("x", width + 20)
            .attr("y", 10)
            .attr("dy", ".35em");
            //.html(config.legend_title);

        var x_number_ticks = x.domain()[1] - x.domain()[0],
            y_number_ticks = y.domain()[1] - y.domain()[0],
            x_tick_array = x.ticks(x_number_ticks),
            y_tick_array = y.ticks(y_number_ticks),
            x_tick_separation = x(x_tick_array[1]) - x(x_tick_array[0]),
            y_tick_separation = y(y_tick_array[1]) - y(y_tick_array[0]);

        // Add an x-axis with label.
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.svg.axis().scale(x).orient("bottom").ticks(x_number_ticks))
          .append("text")
            .attr("class", "label")
            .attr("x", width)
            .attr("y", 30)
            .attr("text-anchor", "end")
            .text("");

        // Add a y-axis with label.
        svg.append("g")
            .attr("class", "y axis")
            .call(d3.svg.axis().scale(y).orient("left").ticks(y_number_ticks))
          .append("text")
            .attr("class", "label")
            .attr("y", -40)
            .attr("dy", ".71em")
            .attr("text-anchor", "end")
            .attr("transform", "rotate(-90)")
            .text("");

        svg.selectAll(".x.axis .tick text")
            .style("font-size", "10px")
            .attr("transform", "translate(" + x_tick_separation / 2 +  ",0)");

        svg.selectAll(".y.axis .tick text")
            .style("font-size", "10px")
            .attr("transform", "translate(0," + y_tick_separation / 2 + ")");

        d3.select(svg.selectAll(".x.axis .tick")[0][x_tick_array.length-1]).attr("visibility","hidden");
        d3.select(svg.selectAll(".y.axis .tick")[0][y_tick_array.length-1]).attr("visibility","hidden");

        svg.append("text")
            .attr("x", (width / 2))
            .attr("y", 0 - (margin.top / 2))
            .attr("text-anchor", "middle")
            .style("font-size", "16px")
            .style("font-weight", "bold")
            .text(config.title);

    });

}
