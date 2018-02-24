var RESTAURANTS_DATA = [];
// foursquare API url's to collect data of 3 different categories
var queries = [
               {url : "https://api.foursquare.com/v2/venues/explore?ll=28.575714,77.199007&section=coffee&oauth_token=3ZNVAWRS13NWEIF4HPDBNGHU5YV5X14GIV4LE54YMUGVRMTG&v=20180213", section : "coffee"},
               {url : "https://api.foursquare.com/v2/venues/explore?ll=28.575714,77.199007&radius=20000&query=historical%20gurudwara&oauth_token=3ZNVAWRS13NWEIF4HPDBNGHU5YV5X14GIV4LE54YMUGVRMTG&v=20180213", section : "religion"},
               {url : "https://api.foursquare.com/v2/venues/explore?ll=28.575714,77.199007&section=food&oauth_token=3ZNVAWRS13NWEIF4HPDBNGHU5YV5X14GIV4LE54YMUGVRMTG&v=20180213", section : "food"}
          ];

// ViewModel object
var app_model;
var map;

// The method called when googlemaps API is loaded
function startApp() {
     for(var query=0;query<queries.length;query++){
          callAPI(queries[query].url, queries[query].section);
     }
     app_model = new ListViewModel();
     ko.applyBindings(app_model);
}

// This functions calls the API and the required data is stored in 'object', then pushed to the global 'RESTAURANTS_DATA' array.
function callAPI(url, section) {
     $.getJSON( url, function( data ) {
          var object = {};
          items = data.response.groups[0].items;
          for (var i = 0; i < items.length; i++) {
               object = {};
               object.name = items[i].venue.name;

               object.category = section;

               object.location = [{}];

               object.location[0].lat = items[i].venue.location.lat;

               object.location[0].lng = items[i].venue.location.lng;

               object.phone = items[i].venue.contact.phone || "";

               object.address = items[i].venue.location.address || "";

               object.formattedAddress = items[i].venue.location.formattedAddress || "";

               object.url = items[i].venue.url || "";

               object.rating = items[i].venue.rating || "";

               RESTAURANTS_DATA.push(object);
          }
     }).done(function(){
          // Update information data
          app_model.information(RESTAURANTS_DATA);
          app_model.initMap();
     }).fail(function() {
          alert("Some error occurred while obtaining the data, please refresh!");
     });
}

// Our ViewModel
function ListViewModel() {

     var self = this;

     this.information = ko.observableArray();

     this.searchTerm = ko.observable("");

     this.largeInfoWindow;

     this.responsive = ko.observable(false);

     this.setResponsiveness = function () {
          document.getElementById('ham').classList.toggle("change");

          if(this.responsive()) {
               document.getElementById('filter_id').style.width = "100%";
               document.getElementById('items').style.width = "100%";
               if(screen.width >= 320 && screen.width < 425)
                    document.getElementById('list').style.width = "46%";
               else if(screen.width >= 425 && screen.width < 1024)
                    document.getElementById('list').style.width = "28%";
               else if(screen.width >=1024)
                    document.getElementById('list').style.width = "16%";
               document.getElementById('map').style.width = "100%";
               $('#name_id').html("Neighborhood Map");
               $('#search_id').show();
               this.responsive(false);
          }

          else {
               document.getElementById('filter_id').style.width = "0px";
               document.getElementById('items').style.width = "0px";
               document.getElementById('list').style.width = "0px";
               document.getElementById('map').style.width = "100%";
               $('#name_id').html("");
               $('#search_id').hide();
               this.responsive(true);
          }
     };

     // The filter function which has 2 features
     //   1. Filter the List as displayed
     //   2. Enable/Disable marker points on map
     this.filteredList = ko.computed( function() {
		var filter = self.searchTerm().toLowerCase();
		if (!filter) {
			self.information().forEach(function(locationItem){
                    if(locationItem.marker)
                         locationItem.marker.setVisible(true);
			});
			return self.information();
		} else {
			return ko.utils.arrayFilter(self.information(), function(locationItem) {
				var string = locationItem.name.toLowerCase();
                    var result;
                    if (string.search(filter) >= 0) {
                         locationItem.marker.setVisible(true);
                         result = (string.search(filter) >= 0);
                    } else {
                         locationItem.marker.setVisible(false);
                    }
				return result;
			});
		}
     }, self);

     // Function which opens the marker's infoWindow when an item from the list is clicked
     this.openMarker = function () {
          self.populateInfoWindow(this.marker, self.largeInfoWindow);
          this.marker.setAnimation(google.maps.Animation.BOUNCE);
          setTimeout((function() {
               this.marker.setAnimation(null);
          }).bind(this), 1400);
     };
     this.addOnMarker = function () {
          self.populateInfoWindow(this, self.largeInfoWindow);
          this.setAnimation(google.maps.Animation.BOUNCE);
          setTimeout((function() {
               this.setAnimation(null);
          }).bind(this), 1400);
     };

     // This function opens up the infoWindow, it is called from two points
     //   1. When the ListItem is clicked
     //   2. When the marker is clicked
     // When clicked twice in either case the infoWindow closes.
     this.populateInfoWindow = function (marker, infowindow) {
          var place;
          for (var i = 0; i < self.information().length; i++) {
               if(marker == self.information()[i].marker)
                    place = self.information()[i];
          }
          if (infowindow.marker != marker) {
               infowindow.setContent('');
               infowindow.marker = marker;
               var f_address="";
               if(place.formattedAddress)
                    for(j=0;j<place.formattedAddress.length;j++){
                         f_address += place.formattedAddress[j];
                         if(j!=place.formattedAddress.length-1){
                              f_address += ", ";
                         }
                    }
               content = '<div><h2>'+ place.name +'</h2>';
               if(place.phone!=="")
                    content+='<p> <b>Phone number : </b>' + place.phone  + '</p>';
               if(place.rating!=="")
                    content+='<p> <b>Rating : </b>' + place.rating  + '</p>';
               if(place.url!=="")
                    content+='<p> <b>Website : </b><a href="' + place.url  + '">'+ place.url +'</a></p>';
               if(f_address!=="")
                    content+='<p> <b>Address : </b>' + f_address  + '</p>';
               content+='</div>';
               infowindow.setContent(content);
               infowindow.open(map, marker);
               infowindow.addListener('closeclick', function() {
                    infowindow.marker = null;
               });
          }
          else {
               infowindow.close();
               infowindow.marker = null;
          }
     };

     this.initMap = function () {

          // Constructor creates a new map.
          map = new google.maps.Map(document.getElementById('map'), {
                    center: {lat: 28.574812, lng: 77.199129},
                    zoom: 13,
                    styles : MAP_STYLE,
                    mapTypeControl: true,
                    mapTypeControlOptions: {
                         style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
                         position: google.maps.ControlPosition.RIGHT_CENTER
                    }
               });

          self.largeInfoWindow = new google.maps.InfoWindow();

          // Plotting markers on the map
          for (var i = 0; i < self.information().length; i++) {

               this.title = self.information()[i].name;

               this.position = self.information()[i].location[0];

               // marker images
               var image;
               if(self.information()[i].category == "coffee")
                    image = 'img/coffee-map.png';
               if(self.information()[i].category == "food")
                    image = 'img/location.png';
               if(self.information()[i].category == "religion")
                    image = 'img/placeholder.png';

               this.marker = new google.maps.Marker({
                    map: map,
                    position: this.position,
                    title: this.title,
                    animation: google.maps.Animation.DROP,
                    icon: image,
                    id: i
               });

               this.marker.setMap(map);

               self.information()[i].marker = this.marker;

               this.marker.addListener('click', self.addOnMarker);
          }
     };
}

onError = function onError() {
    alert('Oops. Google Maps did not load. Please refresh the page and try again!');
};
