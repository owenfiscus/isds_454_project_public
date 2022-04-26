const query_string = window.location.search;
const base_url = "https://nutwoodauto.group/query/new_query_vehicle";
const image_base_url = "https://static.nutwoodauto.group/img";
const image_extension = '.jpg';

const vehicle_wrapper = document.getElementById('vehicle_wrapper');

var url_parameters = new URLSearchParams(query_string);
var vehicle_query_url = `${base_url}?manu=${url_parameters.get('manu')}&car_id=${url_parameters.get('car_id')}`;

// ?car_id=00&manu=manufacturer
console.log(vehicle_query_url);

// pull model data and create options
window.onload = function populate_vehicle_information() {
    make_request(vehicle_query_url)
    .then(function(result) {
        var data = JSON.parse(result);

        // define image url
        var image_url = `${image_base_url}/${data.manufacturer[0].toLowerCase()}_${data.car_id[0]}${image_extension}`
        
        // use placeholder if image doesn't exist
        var xhr = new XMLHttpRequest();
        xhr.open('HEAD', image_url, false);
        xhr.send();
        if (xhr.status == 404) {
            image_url = "https://static.nutwoodauto.group/img/fallback.png"
        }

        // define vehicle name
        var vehicle_name = `${data.manufacturer[0]} ${data.model[0]} ${data.trim_[0]}`;

        // define favorite id
        var favid = 'favid_' + data.manufacturer[0].toLowerCase() + '_' + data.car_id[0];

        // define vehicle specification variables
        var msrp = '$' + data.msrp_price[0];
        var mpg = data.city_mpg[0] + ' / ' + data.highway_mpg[0];
        var engine = data.engine[0];
        var transmission = data.transmission_type[0];
        var drivetrain = data.drivetrain_type[0];
        var height = data.height_in[0] + '"';
        var width = data.width_in[0] + '"';
        var length = data.length_in[0] + '"';
        var wheelbase = data.wheelbase[0] + '"';
        var weight = data.curb_weight[0] + ' lbs';
        var doors = data.door_number[0];
        var fuel_tank = data.fuel_tank_size[0] + ' gal';
        var horsepower = data.horsepower[0];

        // define manufacturer link
        var manufacturer_link = data.web_link[0];

        // html string literal variable
        var vehicle_information = `
          <div id="vehicle_information">
            <div class="vehicle_name"><h1>${vehicle_name}</h1></div>

            <div class="vehicle_information_image vehicle_information_card" onclick="view_large_image('${image_url}')">
              <img src="${image_url}"></img>
            </div>

            <button class="favbtn nuefavbtn" id="vehicle_favbtn" onclick="favorite_vehicle('${favid}', '${data.manufacturer[0]}', '${data.model[0]}', '${data.car_id[0]}')" type="button"><span class="material-icons-round">favorite</span></button>
            
            <div class="vehicle_manufacturer_link vehicle_information_card"><a href="${manufacturer_link}">Manufacturer Website <span class="material-icons-round">launch</span></a></div>

            <div class="vehicle_general vehicle_information_card">
              <h1>General Information</h1>
              <div class="vehicle_spec_row"><p class="vehicle_spec"><span class="material-icons-round">savings</span> MSRP: </p><p class="vehicle_spec">${msrp}</p></div>
              <div class="vehicle_spec_row"><p class="vehicle_spec"><span class="material-icons-round">settings</span> Engine: </p><p class="vehicle_spec">${engine}</p></div>
              <div class="vehicle_spec_row"><p class="vehicle_spec"><span class="material-icons-round">settings</span> Transmission: </p><p class="vehicle_spec">${transmission}</p></div>
              <div class="vehicle_spec_row"><p class="vehicle_spec"><span class="material-icons-round">settings</span> Drivetrain: </p><p class="vehicle_spec">${drivetrain}</p></div>
              <div class="vehicle_spec_row"><p class="vehicle_spec"><span class="material-icons-round">speed</span> Horsepower: </p><p class="vehicle_spec">${horsepower}</p></div>
              <div class="vehicle_spec_row"><p class="vehicle_spec"><span class="material-icons-round">propane_tank</span> Tank size: </p><p class="vehicle_spec">${fuel_tank}</p></div>
              </div>

            <div class="vehicle_dimensions vehicle_information_card">
              <h1>Dimensions</h1>
              <div class="vehicle_spec_row"><p class="vehicle_spec"><span class="material-icons-round">square_foot</span> Height: </p><p class="vehicle_spec">${height}</p></div>
              <div class="vehicle_spec_row"><p class="vehicle_spec"><span class="material-icons-round">square_foot</span> Width: </p><p class="vehicle_spec">${width}</p></div>
              <div class="vehicle_spec_row"><p class="vehicle_spec"><span class="material-icons-round">square_foot</span> Length: </p><p class="vehicle_spec">${length}</p></div>
              <div class="vehicle_spec_row"><p class="vehicle_spec"><span class="material-icons-round">square_foot</span> Wheelbase: </p><p class="vehicle_spec">${wheelbase}</p></div>
              <div class="vehicle_spec_row"><p class="vehicle_spec"><span class="material-icons-round">drive_eta</span> Curb Weight: </p><p class="vehicle_spec">${weight}</p></div>
              <div class="vehicle_spec_row"><p class="vehicle_spec"><span class="material-icons-round">sensor_door</span> Number of doors: </p><p class="vehicle_spec">${doors}</p></div>
            </div>`;

        // append element
        vehicle_wrapper.insertAdjacentHTML('beforeend', vehicle_information);

        // add favorited class to button if vehicle is favorited
        var local_data = JSON.parse(localStorage.getItem(favid.toString()));
        // only perform the check if the data is available
        if (local_data != null || undefined && local_data.set == 1 && document.getElementById('vehicle_favbtn')) {
            $('#vehicle_favbtn').addClass('favorited');
        }
    });
}

// make a get request to a provided endpoint
function make_request(url) {
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

// show large image modal
function view_large_image(url) {
  var large_img_modal = `
                        <div class="large_img_modal" id="large_vehicle_image">
                          <div class="large_img_wrap">
                            <div class="large_img_btn_bg"><button id="close_large_img" class="closebtn nueclosebtn large_img_close" onclick="closeimage()" type="button" ><span class="material-icons-round">close</span></button></div>
                            <img src="${url}"></img>
                          </div>
                        </div>`

  vehicle_wrapper.insertAdjacentHTML('beforeend', large_img_modal);
  $("#vehicle_information").fadeOut(200);
  $(".large_img_modal").fadeIn(200);
}

// close large image modal
function closeimage() {
  $("#vehicle_information").fadeIn(200);
  $(".large_img_modal").fadeOut(200);
  // remove the image modal after the fadeout
  setTimeout(() => {  $(".large_img_modal").remove(); }, 200);
}

// favorite vehicle
function favorite_vehicle(id, manufacturer, model, car_id) {
  var faved = JSON.parse(localStorage.getItem(id));
  if (faved != null || undefined && faved.set == 1) {
    $('.favbtn').removeClass('favorited');
    localStorage.setItem(id , null);
  } else {
    $('.favbtn').addClass('favorited');
    stored_data = {'set': 1, 'manufacturer': manufacturer, 'model': model, 'car_id': car_id};
    localStorage.setItem(id, JSON.stringify(stored_data));
  }
}