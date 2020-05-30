var graphData = air_data;

// set the dimensions and margins of the graph
var margin = {top: 30, right: 10, bottom: 20, left: 30},
	width = 400 - margin.left - margin.right,
	height = 400 - margin.top - margin.bottom;

var strictIsoParse = d3.utcParse("%Y-%m-%dT%H:%M:%S")


function draw(data) {

	if(variable == "airquality") {
		d3.select("#iaq_index")
			.style('display', 'block !important');
	}

	// append the svg object to the body of the page
	var svg = d3.select("#plot")
	  .append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
	  .append("g")
		.attr("transform",
			  "translate(" + margin.left + "," + margin.top + ")");

	svg.append("text")
		.attr("x", (width / 2))
		.attr("y", (0 - margin.top / 2))
		.attr("text-anchor", "middle")
		.style("font-size", "16px")
		.style("fill", "white")
		.style("text-decoration", "bold")
		.text(function(d) {
			if(variable == "temperature")
				return "Temperature [ºC]";
			else if(variable == "pressure")
				return "Pressure [hPa]";
			else if(variable == "humidity")
				return "Humidity [%]";
			else if(variable == "airquality")
				return "Air Quality Index [0-500]";
		});

	// Add X axis --> it is a date format
	var x = d3.scaleTime()
		.domain(d3.extent(data, function(d) { return strictIsoParse(d.timestamp); }))
		.range([ 0, width ]);

	var axis_x = d3.axisBottom()
		.scale(x)
		.ticks(6)
		.tickSize(6, 0)
		.tickFormat(d3.timeFormat("%d/%m"));

	var  xAxis = svg.append("g")
		.attr("transform", "translate(0," + height + ")")
		.call(axis_x);

	// Add Y axis
	var y = d3.scaleLinear()
		.domain([
		0.90*d3.min(data, function(d) {
			if(variable == "temperature")
				return +(d.temperature);
			else if(variable == "pressure")
				return +(d.pressure);
			else if(variable == "humidity")
				return +(d.humidity);
			else if(variable == "airquality")
				return 0;
		})		,
		1.10*d3.max(data, function(d) {
			if(variable == "temperature")
				return +(d.temperature);
			else if(variable == "pressure")
				return +(d.pressure);
			else if(variable == "humidity")
				return +(d.humidity);
			else if(variable == "airquality")
				return +(d.airq);
		})
		])
		.range([ height, 0 ]);

	svg.append("g")
		.call(d3.axisLeft(y));

	// Add a clipPath: everything out of this area won't be drawn.
	var clip = svg.append("defs").append("svg:clipPath")
		.attr("id", "clip")
		.append("svg:rect")
		.attr("width", width )
		.attr("height", height )
		.attr("x", 0)
		.attr("y", 0);

	// Add brushing
	var brush = d3.brushX()                   // Add the brush feature using the d3.brush function
		.extent( [ [0,0], [width,height] ] )  // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
		.on("end", updateChart)               // Each time the brush selection changes, trigger the 'updateChart' function

	// Create the line variable: where both the line and the brush take place
	var line = svg.append('g')
	  .attr("clip-path", "url(#clip)")


	// Add the line
	line.append("path")
	  .datum(data)
	  .attr("fill", "none")
	  .attr("class", "line")
	  .attr("stroke", "steelblue")
	  .attr("stroke-width", 1.5)
	  .attr("d", d3.line()
		.x(function(d) { return x(strictIsoParse(d.timestamp)) })
		.y(function(d) {
			if(variable == "temperature")
				return y(d.temperature);
			else if(variable == "pressure")
				return y(d.pressure);
			else if(variable == "humidity")
				return y(d.humidity);
			else if(variable == "airquality")
				return y(d.airq);
		})
		);

	// Add the brushing
	line
	  .append("g")
		.attr("class", "brush")
		.call(brush);

	// A function that set idleTimeOut to null
	var idleTimeout;
	function idled() { idleTimeout = null; }

	// A function that update the chart for given boundaries
	function updateChart() {

		// What are the selected boundaries?
		extent = d3.event.selection

		// If no selection, back to initial coordinate. Otherwise, update X axis domain
		if(!extent){
			if (!idleTimeout) return idleTimeout = setTimeout(idled, 350); // This allows to wait a little bit
			x.domain([ 4,8])
		} else{
			x.domain([ x.invert(extent[0]), x.invert(extent[1]) ])
			line.select(".brush").call(brush.move, null) // This remove the grey brush area as soon as the selection has been done
		}

		// Update axis and line position
		xAxis.transition().duration(1000).call(d3.axisBottom(x))

		line
			.select('.line')
			.transition()
			.duration(1000)
			.attr("d", d3.line()
			.x(function(d) { return x(strictIsoParse(d.timestamp)) })
			.y(function(d) {
				if(variable == "temperature")
					return y(d.temperature);
				else if(variable == "pressure")
					return y(d.pressure);
				else if(variable == "humidity")
					return y(d.humidity);
				else if(variable == "airquality")
					return y(d.airq);
			})
			);
	}

	// If user double click, reinitialize the chart
	svg.on("dblclick",function(){
		x.domain(d3.extent(data, function(d) { return strictIsoParse(d.timestamp); }))
		xAxis.transition().call(d3.axisBottom(x))
		line
			.select('.line')
			.transition()
			.duration(1000)
			.attr("d", d3.line()
			.x(function(d) { return x(strictIsoParse(d.timestamp)) })
			.y(function(d) {
				if(variable == "temperature")
					return y(d.temperature);
				else if(variable == "pressure")
					return y(d.pressure);
				else if(variable == "humidity")
					return y(d.humidity);
				else if(variable == "airquality")
					return y(d.airq);
			})
			);
	});
}

draw(graphData);