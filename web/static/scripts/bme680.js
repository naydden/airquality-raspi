var graphData = air_data;
console.log(graphData)
// set the dimensions and margins of the graph
var margin = {top: 30, right: 10, bottom: 20, left: 30},
	width = 250 - margin.left - margin.right,
	height = 200 - margin.top - margin.bottom;

var strictIsoParse = d3.utcParse("%Y-%m-%dT%H:%M:%S")


function drawTemperature(data) {
	// append the svg object to the body of the page
	var svg = d3.select("#temperature")
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
		.text("Temperature [ºC]");

	// Add X axis --> it is a date format
	var x = d3.scaleTime()
		.domain(d3.extent(data, function(d) { return strictIsoParse(d.timestamp); }))
		.range([ 0, width ]);
	svg.append("g")
		.attr("transform", "translate(0," + height + ")")
		.call(d3.axisBottom(x));

	// Add Y axis
	var y = d3.scaleLinear()
		.domain([0, d3.max(data, function(d) { return +(d.temperature); })])
		.range([ height, 0 ]);
	svg.append("g")
		.call(d3.axisLeft(y));

	// Add the line
	svg.append("path")
	  .datum(data)
	  .attr("fill", "none")
	  .attr("stroke", "steelblue")
	  .attr("stroke-width", 1.5)
	  .attr("d", d3.line()
		.x(function(d) { return x(strictIsoParse(d.timestamp)) })
		.y(function(d) { return y(d.temperature) })
		)
}

function drawPressure(data) {
	// append the svg object to the body of the page
	var svg = d3.select("#pressure")
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
		.text("Pressure [hPa]");

	// Add X axis --> it is a date format
	var x = d3.scaleTime()
		.domain(d3.extent(data, function(d) { return strictIsoParse(d.timestamp); }))
		.range([ 0, width ]);
	svg.append("g")
		.attr("transform", "translate(0," + height + ")")
		.call(d3.axisBottom(x));

	// Add Y axis
	var y = d3.scaleLinear()
		.domain([0, d3.max(data, function(d) { return +d.pressure; })])
		.range([ height, 0 ]);
	svg.append("g")
		.call(d3.axisLeft(y));

	// Add the line
	svg.append("path")
	  .datum(data)
	  .attr("fill", "none")
	  .attr("stroke", "steelblue")
	  .attr("stroke-width", 1.5)
	  .attr("d", d3.line()
		.x(function(d) { return x(strictIsoParse(d.timestamp)) })
		.y(function(d) { return y(d.pressure) })
		)
}

function drawHumidity(data) {
	// append the svg object to the body of the page
	var svg = d3.select("#humidity")
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
		.text("Humidity [%]");

	// Add X axis --> it is a date format
	var x = d3.scaleTime()
		.domain(d3.extent(data, function(d) { return strictIsoParse(d.timestamp); }))
		.range([ 0, width ]);
	svg.append("g")
		.attr("transform", "translate(0," + height + ")")
		.call(d3.axisBottom(x));

	// Add Y axis
	var y = d3.scaleLinear()
		.domain([0, d3.max(data, function(d) { return +d.humidity; })])
		.range([ height, 0 ]);
	svg.append("g")
		.call(d3.axisLeft(y));

	// Add the line
	svg.append("path")
	  .datum(data)
	  .attr("fill", "none")
	  .attr("stroke", "steelblue")
	  .attr("stroke-width", 1.5)
	  .attr("d", d3.line()
		.x(function(d) { return x(strictIsoParse(d.timestamp)) })
		.y(function(d) { return y(d.humidity) })
		)
}

function drawAirQuality(data) {
	// append the svg object to the body of the page
	var svg = d3.select("#airquality")
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
		.text("Air Quality [0-100 index]");

	// Add X axis --> it is a date format
	var x = d3.scaleTime()
		.domain(d3.extent(data, function(d) { return strictIsoParse(d.timestamp); }))
		.range([ 0, width ]);
	svg.append("g")
		.attr("transform", "translate(0," + height + ")")
		.call(d3.axisBottom(x));

	// Add Y axis
	var y = d3.scaleLinear()
		.domain([0, d3.max(data, function(d) { return +d.airq; })])
		.range([ height, 0 ]);
	svg.append("g")
		.call(d3.axisLeft(y));

	// Add the line
	svg.append("path")
	  .datum(data)
	  .attr("fill", "none")
	  .attr("stroke", "steelblue")
	  .attr("stroke-width", 1.5)
	  .attr("d", d3.line()
		.x(function(d) { return x(strictIsoParse(d.timestamp)) })
		.y(function(d) { return y(d.airq) })
		)
}

drawTemperature(graphData);
drawPressure(graphData);
drawHumidity(graphData);
drawAirQuality(graphData);
