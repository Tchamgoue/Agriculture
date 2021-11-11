var demo=true;

var base_maker=false;

if (demo==true){
    var colormap=L.map("map", {
        center : [ 5.4527263, 10.0268688 ],
        zoom :34
    }).flyTo([ 5.4527263, 10.0268688 ], 7);
}
else{
    var colormap=L.map("map", {
        center : [ 3.811969898599434, 11.513855999999999 ],
        zoom :1
    }).setView([ 3.811969898599434, 11.513855999999999 ], 1);
}
//var map_url="https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png"
var map_url="https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw"
L.tileLayer(map_url, {
		maxZoom: 200,
		attribution: 'Agro-ecology similarity',
		id: 'mapbox/light-v9',
		tileSize: 512,
		zoomOffset: -1
	}).addTo(colormap);

(function($) {
    $(function(e){
        function getRandomIntInclusive(min, max) {
                    min = Math.ceil(min);
                    max = Math.floor(max);
                    return Math.floor(Math.random() * (max - min +1)) + min;
        }

        function getColor(feature){
            var array_color=["#e9fbec","#bdf4c6","#91eda0","#65e67a","#39df54","#20c63a","#199a2d","#126e20","#0b4213","#041606"]
            var rand_number=getRandomIntInclusive(0,array_color.length-1)
            return array_color[rand_number];
        }
function findStyle(feature) {
    return {
        fillColor: getColor(feature.properties.density),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}


$("#longitude").val("5.4527263");
$("#latitude").val("10.0268688")


//.geoJson(all_country_geojson,{style:findStyle}).addTo(colormap);
if (demo==true){
    var marker=L.marker([ 5.4527263, 10.0268688])
}
else{
    var marker=L.marker([3.811969898599434,11.53788859277347]);
}


var markers=[]
markers.push(marker);
//alert("Bonjour");
markers[0].addTo(colormap);

//L.geoJson(cameroon_cart,{style:findStyle}).addTo(colormap);
//L.geoson(cameroon_cart).addTo(colormap);

/*var circle = L.circle([51.505, 11.53788859277347], {radius: 1000000,  color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5},).addTo(colormap);*/

colormap.on("click", function(e){
                    var marker_temp=L.marker([e.latlng.lat,e.latlng.lng]);
                    if (base_maker==false){
                        colormap.removeLayer(markers[0]);
                        markers[0]=marker_temp;
                    }
                    else {
                        markers.push(marker_temp)
                    }
                    markers[markers.length-1].addTo(colormap);
                    //alert(markers.length)
					var p=e.latlng;
					
					$("#latitude").val(p.lat.toString());
					$("#longitude").val(p.lng.toString());
				});
        $("#btnmake_base").click(function(event){
            base_maker=true;
            //alert("Clicking");
        });
        $("#rase-all").click(function(event){
            base_maker=false;
            for (i=1;i<markers.length;i++){
                colormap.removeLayer(markers[i]);
            }
            markers=[markers[0]]
        });
    });
   // bonou
   $("#form-similarity").on("submit",function(evt){

       evt.preventDefault();
       $("#pageloader .loader-text").html("<h3 style='color:#fff'>Similarity computation in progress...</h3>")
       $("#pageloader").fadeIn();

        var longitude=$("#longitude").val();
        var latitude=$("#latitude").val();
        var urlold='http://62.171.170.214:8000 '

        var action_url="http://62.171.170.214:8000/api/analogy_climate"

        if (demo==true){
            let location=window.location;
            let root_url=location.protocol+"//"+location.host
            action_url=$("#demo-url").text()
            
        }

        var demo_color=["#fefb01","#cefb02","#87fa00","#3af901","#00ed01"]
        
        var settings = {
        "url": action_url,
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "text/plain"
        },
        "data": "{\r\n    \"source_lat\":"+latitude+",\r\n    \"source_long\":"+longitude+",\r\n    \"refs\": [\r\n        {\r\n            \"lat\": 2.343,\r\n            \"long\": 5.231\r\n        },\r\n        {\r\n            \"lat\": 3.233,\r\n            \"long\": 5.234\r\n        }\r\n    ]\r\n}",
        };
        
        if (demo==true){
            settings["data"]["demo"]=true;
            //settings["data"]["csrfmiddlewaretoken"]=$("input[name=csrfmiddlewaretoken]").val()
            //settings["data"]=new FormData(this);
            //alert(settings["csrfmiddlewaretoken"])
        }

        $.ajax(settings).done(function (response) {
            $("#pageloader").fadeOut();
            console.log("Success");
[0,1,2,3,4]
            if (demo==true){
                var intervals=response["intervals"]
                var length_list=intervals.length;
                for(var i=0;i<response["point"].length;i++){
                    // Cette boucle va permettre de determine
                    var current_indice=response["point"][i]["indice"]
                    var trouve=-1;
                    var j=0;
                    while (trouve==-1 && j<length_list-1){
                        if(current_indice>=intervals[j] && current_indice<intervals[j+1]){
                            trouve=j;
                        }
                        j=j+1;
                    }
                    if (trouve==-1){
                        trouve=length_list-1
                    }
                    var circle = L.circle([response["point"][i]["lat"],response["point"][i]["long"]], {radius: 50,  color: demo_color[trouve],
                                fillColor: demo_color[trouve],
                                fillOpacity: 0.1},).addTo(colormap);
                }
                // Maintenant nous allons selectionner un point aleatoire dans le systeme
                // et zoommer dessus
                min=Math.ceil(intervals[0])
                max=Math.floor(intervals[length_list-1] )
                var random_point= Math.ceil(Math.random() * (max - min+ 1)) + min;
                //alert(random_point)
                colormap.flyTo([ response["point"][random_point]["lat"],response["point"][random_point]["long"]], 10);

            }
            else{
                for(var i=0;i<response.length;i++){
                    var circle = L.circle([response[i][0], response[i][1]], {radius: 10000,  color: 'green',
                                fillColor: 'green',
                                fillOpacity: 0.5},).addTo(colormap);
                }
            }
            
            console.log(response);
            //alert(response);
        }).fail(function(response){
            
            alert("Similarity fail")
            $("#pageloader").fadeOut();
            console.log(response);
        });
        /* $.ajax({
            url:"http://62.171.170.214:8000/api/analogy_climate",
            method:"POST",
            timeout:0,
            contentType: false,
            cache: false,
            processData: false,
            dataType: "json",
            headers:{"Content-type":"text/plain"},
            data:{
                "source_lat":latitude,
                "source_long":longitude,
                "refs":[]
            },
            success:function(result){
                $("#pageloader").fadeOut();
                alert("Similarity perform with success");
            },
            error:function(result){
                $("#pageloader").fadeOut();
                alert("Error during similarity performing");
            }
        });*/

   });
})(jQuery);