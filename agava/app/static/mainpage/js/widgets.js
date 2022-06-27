function f(csv){
    const margin = {top: 10, right: 30, bottom: 30, left: 60},
        width = 1000 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    const svg = d3.select("#my_dataviz")
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

        const x = d3.scaleTime()
          .domain(d3.extent(data, function(d) { return d.date; }))
          .range([ 0, width ]);
        xAxis = svg.append("g")
          .attr("transform", `translate(0, ${height})`)
          .call(d3.axisBottom(x));

        const y = d3.scaleLinear()
          .domain([0, d3.max(data, function(d) { return +d.value; })])
          .range([ height, 0 ]);
        yAxis = svg.append("g")
          .call(d3.axisLeft(y));

        const clip = svg.append("defs").append("svg:clipPath")
            .attr("id", "clip")
            .append("svg:rect")
            .attr("width", width )
            .attr("height", height )
            .attr("x", 0)
            .attr("y", 0);

        const brush = d3.brushX()
            .extent( [ [0,0], [width,height] ] )
            .on("end", updateChart)

        const line = svg.append('g')
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
        });
    })
}