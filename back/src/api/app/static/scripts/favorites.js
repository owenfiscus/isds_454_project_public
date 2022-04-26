// consts
const endpoint = "https://nutwoodauto.group/query/json_simple"
const vehicle_base_url = "https://nutwoodauto.group/vehicle";
const favorites = document.getElementById('favorites_wrapper');
const manufacturer = {1:"toyota", 2:"ford", 3:"honda", 4:"subaru", 5:"lamborghini", 6:"bmw", 7:"mercedes", 8:"ferrari"};

// vars
var manu = "?manu=";
var model = "&model="

var c = 0;

// hide the placeholder text by default
$('#placeholder').css("display", "none");

// get data function to pull json from db
function getdata(url) {
    return new Promise(function(resolve, reject) {
      var xhr = new XMLHttpRequest();
      xhr.onload = function() {
        resolve(this.responseText);
      };
      xhr.onerror = reject;
      xhr.open('GET', url);
      xhr.send();
  });
}

// remels function removes created elements
function rmels(parent){
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
  }
}

// generate favorites list
window.onload = function() {
  var id = Math.random().toString().slice(2,18);

  // remove old elements
  rmels($('#favorites_wrapper'));

  // runs for each vehicle manufacturer in the manufacturer object
  for (const property in manufacturer) {
    c++;
    getdata(`${endpoint}${manu}${manufacturer[property]}`)
        .then(function(result) {
          var data = JSON.parse(result);
          var count = Object.keys(data.car_id).length;
          for (let i = 0; i <= count; i++) {
            
            // get the name of the vehicle
            var text = data.manufacturer[i] + " " + data.model[i] + " " + data.trim_[i];

            // generate the favorite list item
            var favorite_id = 'favid_' + data.manufacturer[i].toLowerCase() + '_' + (data.car_id[i]);
            var favorite_box_id = 'favorite_box_id_' + data.manufacturer[i].toLowerCase() + '_' + (i + 1);
            var vehicle_page_url = `${vehicle_base_url}?manu=${data.manufacturer[i]}&car_id=${data.car_id[i]}`;

            var favorite = `
            <div id="${favorite_box_id}" class="favorite_box">
              <li class="favorite" id="${favorite_id}"><span class="material-icons-round">favorite</span> ${text}</li>
              <div class="favorite_vehicle_link"><a href="${vehicle_page_url}">Vehicle Page <span class="material-icons-round">launch</span></a></div>
            </div>
            `;

            // pull local favorites data
            var local_id = favorite_id.toString();
            var local_data = JSON.parse(localStorage.getItem(local_id));

            // add the favorite list item if it exists
            if (local_data != null) {
              favorites.insertAdjacentHTML('beforeend', favorite)
              console.log(favorite_id);
            }
          }
        })
        .catch(function() {
          // check if favorites exist
          var elements = $('.favorite').length;
          if (elements == 0 && c == manufacturer.length) {
            // show if no favorites exist
            $('#placeholder').fadeIn(200);
          }
        });
    }
  }