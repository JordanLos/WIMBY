/**** Get Array of Locations from JSON  ****/
	var sites = []
	$.getJSON('./data/Contaminated-Sites-In-Edmonton.json', function( data ) {
		$.each( data, function(i) {
			sites.push( data[i] );
		})
		// Updates the Number based on the size of the array
		$('#number').fadeOut( function() {
			$(this).text(sites.length).fadeIn();
		});
	});



	var map, map2;
	function initMap() {
		// Create Heatmap for Ladning Page
		map = new google.maps.Map(document.getElementById('map'), {
			zoom: 12,
			center: {lat: 53.5334573, lng: -113.4909777},
			styles: [
			  {
				"elementType": "geometry",
				"stylers": [
				  {
					"color": "#1d2c4d"
				  }
				]
			  },
			  {
				"elementType": "labels.text.fill",
				"stylers": [
				  {
					"color": "#8ec3b9"
				  }
				]
			  },
			  {
				"elementType": "labels.text.stroke",
				"stylers": [
				  {
					"color": "#1a3646"
				  }
				]
			  },
			  {
				"featureType": "administrative.country",
				"elementType": "geometry.stroke",
				"stylers": [
				  {
					"color": "#4b6878"
				  }
				]
			  },
			  {
				"featureType": "administrative.land_parcel",
				"elementType": "labels.text.fill",
				"stylers": [
				  {
					"color": "#64779e"
				  }
				]
			  },
			  {
				"featureType": "administrative.province",
				"elementType": "geometry.stroke",
				"stylers": [
				  {
					"color": "#4b6878"
				  }
				]
			  },
			  {
				"featureType": "landscape.man_made",
				"elementType": "geometry.stroke",
				"stylers": [
				  {
					"color": "#334e87"
				  }
				]
			  },
			  {
				"featureType": "landscape.natural",
				"elementType": "geometry",
				"stylers": [
				  {
					"color": "#023e58"
				  }
				]
			  },
			  {
				"featureType": "poi",
				"elementType": "geometry",
				"stylers": [
				  {
					"color": "#283d6a"
				  }
				]
			  },
			  {
				"featureType": "poi",
				"elementType": "labels.text.fill",
				"stylers": [
				  {
					"color": "#6f9ba5"
				  }
				]
			  },
			  {
				"featureType": "poi",
				"elementType": "labels.text.stroke",
				"stylers": [
				  {
					"color": "#1d2c4d"
				  }
				]
			  },
			  {
				"featureType": "poi.park",
				"elementType": "geometry.fill",
				"stylers": [
				  {
					"color": "#023e58"
				  }
				]
			  },
			  {
				"featureType": "poi.park",
				"elementType": "labels.text.fill",
				"stylers": [
				  {
					"color": "#3C7680"
				  }
				]
			  },
			  {
				"featureType": "road",
				"elementType": "geometry",
				"stylers": [
				  {
					"color": "#304a7d"
				  }
				]
			  },
			  {
				"featureType": "road",
				"elementType": "labels.text.fill",
				"stylers": [
				  {
					"color": "#98a5be"
				  }
				]
			  },
			  {
				"featureType": "road",
				"elementType": "labels.text.stroke",
				"stylers": [
				  {
					"color": "#1d2c4d"
				  }
				]
			  },
			  {
				"featureType": "road.highway",
				"elementType": "geometry",
				"stylers": [
				  {
					"color": "#2c6675"
				  }
				]
			  },
			  {
				"featureType": "road.highway",
				"elementType": "geometry.stroke",
				"stylers": [
				  {
					"color": "#255763"
				  }
				]
			  },
			  {
				"featureType": "road.highway",
				"elementType": "labels.text.fill",
				"stylers": [
				  {
					"color": "#b0d5ce"
				  }
				]
			  },
			  {
				"featureType": "road.highway",
				"elementType": "labels.text.stroke",
				"stylers": [
				  {
					"color": "#023e58"
				  }
				]
			  },
			  {
				"featureType": "transit",
				"elementType": "labels.text.fill",
				"stylers": [
				  {
					"color": "#98a5be"
				  }
				]
			  },
			  {
				"featureType": "transit",
				"elementType": "labels.text.stroke",
				"stylers": [
				  {
					"color": "#1d2c4d"
				  }
				]
			  },
			  {
				"featureType": "transit.line",
				"elementType": "geometry.fill",
				"stylers": [
				  {
					"color": "#283d6a"
				  }
				]
			  },
			  {
				"featureType": "transit.station",
				"elementType": "geometry",
				"stylers": [
				  {
					"color": "#3a4762"
				  }
				]
			  },
			  {
				"featureType": "water",
				"elementType": "geometry",
				"stylers": [
				  {
					"color": "#0e1626"
				  }
				]
			  },
			  {
				"featureType": "water",
				"elementType": "labels.text.fill",
				"stylers": [
				  {
					"color": "#4e6d70"
				  }
				]
			  }
			]
		});

		// dynamically load the GeoJSON data
		var script = document.createElement('script');
		script.src = './data/Contaminated-Sites-In-Edmonton.geojsonp';
		document.getElementsByTagName('head')[0].appendChild(script);
		
		map2 = new google.maps.Map(document.getElementById('map2'), {
			zoom: 12,
			center: {lat: 53.5334573, lng: -113.4909777}
		});

		
	}
	window.eqfeed_callback = function(results) {
	// Loop the data returned from the GeoJSON eqfeed_callback
	// and create a marker for each coordinate
		var heatmapData = [];
		var infowindow = new google.maps.InfoWindow({
			content: 'holding'
		});

		for (var i = 0; i < results.features.length; i++) {
			var coords = results.features[i].geometry.coordinates;
			var latLng = new google.maps.LatLng(coords[1],coords[0]);
			var marker = new google.maps.Marker({
				position: latLng,
				map: map2,
				html: sites[i].house + ' ' + sites[i].street + "<br><a target='_blank' href='http://www.esar.alberta.ca/esarmain.aspx'>Plan:  " + sites[i].plan + "<br>Block: " + sites[i].block + "<br>Lot:   " + sites[i].block
			});

			heatmapData.push(latLng);

			marker.addListener('click', function() {
				console.log('you clicked!'),
				infowindow.setContent(this.html);
				infowindow.open(map2, this);
			});

				
		}
		var gradient = [
		  'rgba(0, 255, 255, 0)',
		  'rgba(0, 255, 255, 1)',
		  'rgba(0, 191, 255, 1)',
		  'rgba(0, 127, 255, 1)',
		  'rgba(0, 63, 255, 1)',
		  'rgba(0, 0, 255, 1)',
		  'rgba(0, 0, 223, 1)',
		  'rgba(0, 0, 191, 1)',
		  'rgba(0, 0, 159, 1)',
		  'rgba(0, 0, 127, 1)',
		  'rgba(63, 0, 91, 1)',
		  'rgba(127, 0, 63, 1)',
		  'rgba(191, 0, 31, 1)',
		  'rgba(255, 0, 0, 1)'
		]
		var heatmap = new google.maps.visualization.HeatmapLayer({
			data: heatmapData,
			dissipating: false,
			opacity: 0.3,
			gradient: gradient,
			map: map
		});
	}


