function f(csv, target, wdth, hght){
    var margin = {top: 10, right: 30, bottom: 30, left: 60},
        width = wdth - margin.left - margin.right,
        height = hght - margin.top - margin.bottom;

    var svg = d3.select(target)
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              `translate(${margin.left}, ${margin.top})`);

    d3.csv(csv,

      function(d){
        return { date : d3.timeParse("%Y-%m-%d")(d.date), value : d.value }
      }).then(

      function(data) {

        var x = d3.scaleTime()
          .domain(d3.extent(data, function(d) { return d.date; }))
          .range([ 0, width ]);
        xAxis = svg.append("g")
          .attr("transform", `translate(0, ${height})`)
          .call(d3.axisBottom(x));

        var y = d3.scaleLinear()
          .domain([0, d3.max(data, function(d) { return +d.value; })])
          .range([ height, 0 ]);
        yAxis = svg.append("g")
          .call(d3.axisLeft(y));

        var clip = svg.append("defs").append("svg:clipPath")
            .attr("id", "clip")
            .append("svg:rect")
            .attr("width", width )
            .attr("height", height )
            .attr("x", 0)
            .attr("y", 0);

        var brush = d3.brushX()
            .extent( [ [0,0], [width,height] ] )
            .on("end", updateChart)

        var line = svg.append('g')
          .attr("clip-path", "url(#clip)")

        line.append("path")
          .datum(data)
          .attr("class", "line")
          .attr("fill", "none")
          .attr("stroke", "steelblue")
          .attr("stroke-width", 1.5)
          .attr("d", d3.line()
            .x(function(d) { return x(d.date) })
            .y(function(d) { return y(d.value) })
            )

        line
          .append("g")
            .attr("class", "brush")
            .call(brush);

        let idleTimeout
        function idled() { idleTimeout = null; }

        function updateChart(event,d) {

          extent = event.selection


          if(!extent){
            if (!idleTimeout) return idleTimeout = setTimeout(idled, 350);
            x.domain([ 4,8])
          }else{
            x.domain([ x.invert(extent[0]), x.invert(extent[1]) ])
            line.select(".brush").call(brush.move, null)
          }

          xAxis.transition().duration(1000).call(d3.axisBottom(x))
          line
              .select('.line')
              .transition()
              .duration(1000)
              .attr("d", d3.line()
                .x(function(d) { return x(d.date) })
                .y(function(d) { return y(d.value) })
              )
        }

        var bisect = d3.bisector(function(d) { return d.x; }).left;

        // Create the circle that travels along the curve of chart
        var focus = svg
          .append('g')
          .append('circle')
            .style("fill", "none")
            .attr("stroke", "black")
            .attr('r', 8.5)
            .style("opacity", 0)

        // Create the text that travels along the curve of chart
        var focusText = svg
          .append('g')
          .append('text')
            .style("opacity", 0)
            .attr("text-anchor", "left")
            .attr("alignment-baseline", "middle")

        svg.on("dblclick",function(){
          x.domain(d3.extent(data, function(d) { return d.date; }))
          xAxis.transition().call(d3.axisBottom(x))
          line
            .select('.line')
            .transition()
            .attr("d", d3.line()
              .x(function(d) { return x(d.date) })
              .y(function(d) { return y(d.value) })
          )
        })
//        .on('mouseover', function(){
//
//        })
        .on('mousemove', function(event, d){
            var x0 = x.invert(event.x);
            var i = bisect(data, x0, 1);
            selectedData = data[i]
            console.log(i);
            focus
              .attr("cx", x(selectedData.x))
              .attr("cy", y(selectedData.y))
            focusText
              .html("x:" + selectedData.x + "  -  " + "y:" + selectedData.y)
              .attr("x", x(selectedData.x)+15)
              .attr("y", y(selectedData.y))
           });
//        .on('mouseout', function(){
//
//        });
    })
}