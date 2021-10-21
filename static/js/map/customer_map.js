var customerMap=null;
function Coordonne(Longitude=null,Latitude=null){
	this.long=Longitude;
	this.lat=Latitude;
}

function initCustomerMap(){
	customerMap=L.map("customer_map",{
	}).setView([3.811969898599434,11.53788859277347],8);
	 L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {
         attribution: 'Carte de geolocation de vos patients',
         minZoom: 1,
         maxZoom: 20
     }).addTo(customerMap);
	 
	 var custLocat=new Array();
	
	
}


window.onload=	initCustomerMap();
