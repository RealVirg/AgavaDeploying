function show_widget(type, data, wdth, hght, target){
  if (type=="line_chart")
  {
    date_value_chart(data, target, wdth, hght)
  }
  else if (type=="last_value")
  {
    last_values(data, target, wdth, hght)
  }
}


function last_values(data, target, wdth, hght){
  var svg = d3.select(target)
    .append("svg")
    .attr("width", wdth)
    .attr("height", hght);

var bars = svg.selectAll(".myBars")
    .data(data)
    .enter()
    .append("rect");

bars.attr("x", 10)
    .attr("y", function(d,i){ return 10 + i*40})
    .attr("width", function(d){ return d})
    .attr("height", 30);

var texts = svg.selectAll(".myTexts")
    .data(data)
    .enter()
    .append("text");

texts.attr("x", function(d){ return d + 16})
    .attr("y", function(d,i){ return 30 + i*40})
    .text(function(d){ return d});
}



function date_value_chart(csv, target, wdth, hght){
  var margin = {top: 10, right: 30, bottom: 30, left: 60},
      width = wdth - margin.left - margin.right,
      height = hght - margin.top - margin.bottom;

  var svg = d3.select(target)
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

  d3.csv(csv,

    function(d){
      return { date : d3.timeParse("%Y-%m-%d")(d.date), value : d.value }
    },

    function(data) {

      var x = d3.scaleTime()
        .domain(d3.extent(data, function(d) { return d.date; }))
        .range([ 0, width ]);
      xAxiss = svg.append("g")
        .attr("transform", "translate(0," + height/2 + ")")
        .call(d3.axisBottom(x));

      var y = d3.scaleLinear()
        .domain([-d3.max(data, function(d){return Math.abs(+d.value)}),
        d3.max(data, function(d) { return Math.abs(+d.value); })])
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

      var idleTimeout
      function idled() { idleTimeout = null; }

      function updateChart() {

        extent = d3.event.selection

        if(!extent){
          if (!idleTimeout) return idleTimeout = setTimeout(idled, 350);
          x.domain([ 4,8])
        }else{
          x.domain([ x.invert(extent[0]), x.invert(extent[1]) ])
          line.select(".brush").call(brush.move, null)
        }

        xAxiss.transition().duration(1000).call(d3.axisBottom(x))
        line
            .select('.line')
            .transition()
            .duration(1000)
            .attr("d", d3.line()
              .x(function(d) { return x(d.date) })
              .y(function(d) { return y(d.value) })
            )
      }
    var bisect = d3.bisector(function(d) { return d.date; }).left;

    var focus = svg
      .append('g')
      .append('line')
        .style("fill", "none")
        .attr("stroke", "black")
        .style("opacity", 0)
    var focus1 = svg
    .append('g')
    .append('circle')
      .style("fill", "black")
      .attr("stroke", "black")
      .attr('r', 4.5)
      .style("opacity", 0)
    var foc = svg
      .append('g')
      .append('line')
        .style("fill", "none")
        .attr("stroke", "black")
        .style("opacity", 0)

    var focusText = svg
      .append('g')
      .append('text')
        .style("opacity", 0)
        .attr("text-anchor", "left")
        .attr("alignment-baseline", "middle")

      svg.on("dblclick",function(){
        x.domain(d3.extent(data, function(d) { return d.date; }))
        xAxiss.transition().call(d3.axisBottom(x))
        line
          .select('.line')
          .transition()
          .attr("d", d3.line()
            .x(function(d) { return x(d.date) })
            .y(function(d) { return y(d.value) })
        )
      })
        .on('mouseover', function(){
            foc.style("opacity", 1)
            focus.style("opacity", 1)
            focus1.style("opacity", 1)
            focusText.style("opacity",1)
         })
         .on('mousemove', function(){
          var x0 = x.invert(Math.round(d3.mouse(this)[0]));
          var i = bisect(data, x0);
          selectedData = data[i];
          format = d3.timeFormat("%Y-%m-%d");
          var change_location_x = 15;
          var change_location_y = -10;
          if (x(selectedData.date) > (width / 2)){
              change_location_x = -220;
            }
          if (y(selectedData.value) > (height / 2)){
              change_location_y = 10;
            }
          focus1
            .attr("cx", x(selectedData.date))
            .attr("cy", y(selectedData.value));
          foc
            .attr("x1", 0)
            .attr("y1", y(selectedData.value))
            .attr("x2", width)
            .attr("y2", y(selectedData.value));
          focus
            .attr("x1", x(selectedData.date)-1)
            .attr("y1", 0)
            .attr("x2", x(selectedData.date)-1)
            .attr("y2", height);
          focusText
            .html("Date:" + format(selectedData.date) + "    " + "Value:" + selectedData.value)
            .attr("x", x(selectedData.date)+change_location_x)
            .attr("y", y(selectedData.value)-change_location_y);
         })
         .on('mouseout', function(){
          foc.style("opacity", 0)
          focus.style("opacity", 0)
          focus1.style("opacity", 0)
          focusText.style("opacity", 0)
         });

  })
}

function pvalue1_value2_chart(csv, target, wdth, hght) { // value1 must be possitive
  var margin = {top: 10, right: 30, bottom: 30, left: 60},
      width = wdth - margin.left - margin.right,
      height = hght - margin.top - margin.bottom;

  var svg = d3.select(target)
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

  d3.csv(csv,

    function(d){
      return { x : d.x, y : d.y }
    },

    function(data) {
      function compare(a, b) {
        if  (parseInt(a.x) < parseInt(b.x)){
          return -1;
        }
        if (parseInt(a.x) > parseInt(b.x)){
          return 1;
        }
        return 0;
      }

      data.sort(compare);

      var x = d3.scaleLinear()
        .domain([0, d3.max(data, function(d) { return Math.abs(+d.x); })])
        .range([ 0, width ]);
      xAxis = svg.append("g")
        .attr("transform", "translate(0," + height/2 + ")")
        .call(d3.axisBottom(x));

      var y = d3.scaleLinear()
        .domain([-d3.max(data, function(d){return Math.abs(+d.y)}), d3.max(data, function(d) { return Math.abs(+d.y); })])
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
          .x(function(d) { return x(d.x) })
          .y(function(d) { return y(d.y) })
          )

      line
        .append("g")
          .attr("class", "brush")
          .call(brush);

      var idleTimeout
      function idled() { idleTimeout = null; }

      function updateChart() {

        extent = d3.event.selection

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
              .x(function(d) { return x(d.x) })
              .y(function(d) { return y(d.y) })
            )
      }
    var bisect = d3.bisector(function(d) { return d.x; }).left;

    var focus = svg
      .append('g')
      .append('line')
        .style("fill", "none")
        .attr("stroke", "black")
        .style("opacity", 0)
    var focus1 = svg
    .append('g')
    .append('circle')
      .style("fill", "black")
      .attr("stroke", "black")
      .attr('r', 4.5)
      .style("opacity", 0)
    var foc = svg
      .append('g')
      .append('line')
        .style("fill", "none")
        .attr("stroke", "black")
        .style("opacity", 0)

    var focusText = svg
      .append('g')
      .append('text')
        .style("opacity", 0)
        .attr("text-anchor", "left")
        .attr("alignment-baseline", "middle")

      svg.on("dblclick",function(){
        x.domain([0, d3.max(data, function(d) { return Math.abs(+d.x); })])
        xAxis.transition().call(d3.axisBottom(x))
        line
          .select('.line')
          .transition()
          .attr("d", d3.line()
            .x(function(d) { return x(d.x) })
            .y(function(d) { return y(d.y) })
        )
      })
        .on('mouseover', function(){
            foc.style("opacity", 1)
            focus.style("opacity", 1)
            focus1.style("opacity", 1)
            focusText.style("opacity",1)
         })
         .on('mousemove', function(){
          var x0 = x.invert(Math.round(d3.mouse(this)[0]));
          var i = bisect(data, x0);
          selectedData = data[i];
          var change_location_x = 15;
          var change_location_y = -10;
          console.log(data)
          if (x(selectedData.x) > (width / 2)){
              change_location_x = -220;
            }
          if (y(selectedData.y) > (height / 2)){
              change_location_y = 10;
            }
          focus1
            .attr("cx", x(selectedData.x))
            .attr("cy", y(selectedData.y));
          foc
            .attr("x1", 0)
            .attr("y1", y(selectedData.y))
            .attr("x2", width)
            .attr("y2", y(selectedData.y));
          focus
            .attr("x1", x(selectedData.x)-1)
            .attr("y1", 0)
            .attr("x2", x(selectedData.x)-1)
            .attr("y2", height);
          focusText
            .html("Value1:" + selectedData.x + "    " + "Value2:" + selectedData.y)
            .attr("x", x(selectedData.x)+change_location_x)
            .attr("y", y(selectedData.y)-change_location_y);
         })
         .on('mouseout', function(){
          foc.style("opacity", 0)
          focus.style("opacity", 0)
          focus1.style("opacity", 0)
          focusText.style("opacity", 0)
         });

  })
}
