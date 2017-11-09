queue()
    .defer(d3.json, "/data")
    .await(makeGraphs);

function makeGraphs(error, recordsJson) {
	
	//Clean data
	var records = recordsJson;
	var dateFormat = d3.time.format("%Y-%m-%d %H:%M:%S");
	
	records.forEach(function(d) {
		d["captured"] = dateFormat.parse(d["captured"]);
		d["gmap_lon"] = +d["gmap_lon"];
		d["gmap_lat"] = +d["gmap_lat"];
	});

	// Define map
	var map = L.map('map');
	var drawMap = function(){
	  
	    map.setView([39.8, -102.4], 4.5);
		mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
		L.tileLayer(
			'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
				attribution: '&copy; ' + mapLink + ' Contributors',
				maxZoom: 15,
			}).addTo(map);

	};

	//Create a Crossfilter instance
	var ndx = crossfilter(records);

	//Define Dimensions
	var topic = ndx.dimension(function(d) { return d["topic"]; });
	var coords = ndx.dimension(function(d) { return L.marker([d["gmap_lat"], d["gmap_lon"]]).addTo(map); });
	var city = ndx.dimension(function(d) { return d["city"]; });
	var allDim = ndx.dimension(function(d) {return d;});


	//Group Data
	var coordsGroup = coords.group().reduceCount();
	var topicGroup = topic.group();
	var cityGroup = city.group();
	var all = ndx.groupAll();
	
	//Charts
    var topicChart = dc.barChart("#topic-chart");
    var cityChart = dc.rowChart("#city-chart");

	topicChart
          .width(450)
          .height(800)
          .x(d3.scale.ordinal())
          .xUnits(dc.units.ordinal)
          .brushOn(false)
          .xAxisLabel('topic')
          .yAxisLabel('posts')
	      .dimension(topic)
	      .group(topicGroup);


    cityChart
      	.width(250)
    	.height(800)
        .dimension(city)
        .group(cityGroup)
        .ordering(function(d) { return -d.value })
        .colors(['#6baed6'])
        .elasticX(true)
        .labelOffsetY(10)
        .xAxis().ticks(4);

	//Draw Map
	drawMap();

	// Update the map if any dc chart get filtered
	dcCharts = [cityChart, topicChart];

	_.each(dcCharts, function (dcChart) {
		dcChart.on("filtered", function (chart, filter) {
			map.eachLayer(function (layer) {
				map.removeLayer(layer)
			}); 
			drawMap();
		});
	});

	dc.renderAll();

};