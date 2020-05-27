var graphData = air_data;
console.log(graphData)
// set the dimensions and margins of the graph
var margin = {top: 30, right: 10, bottom: 20, left: 50},
	width = 250 - margin.left - margin.right,
	height = 200 - margin.top - margin.bottom;

var strictIsoParse = d3.utcParse("%Y-%m-%dT%H:%M:%S")

function draw(data, variable) {
	id = '';
	if(variable == "temperature")
		id = "#temperature";
	else if(variable == "pressure")
		id = "#pressure";
	else if(variable == "humidity")
		id = "#humidity";
	else if(variable == "airquality")
		id = "#airquality";

	// append the svg object to the body of the page
	var svg = d3.select(id)
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
				return "Air Quality Index [0-100]";
		});

	// Add X axis --> it is a date format
	var x = d3.scaleTime()
		.domain(d3.extent(data, function(d) { return strictIsoParse(d.timestamp); }))
		.range([ 0, width ]);

	var xAxis = d3.axisBottom()
		.scale(x)
		.ticks(4)
		.tickSize(6, 0)
		.tickFormat(d3.timeFormat("%d/%m"));

	svg.append("g")
		.attr("transform", "translate(0," + height + ")")
		.call(xAxis);

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

	// Add the line
	svg.append("path")
	  .datum(data)
	  .attr("fill", "none")
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
}

draw(graphData, 'temperature');
draw(graphData, 'pressure');
draw(graphData, 'humidity');
draw(graphData, 'airquality');