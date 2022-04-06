// consts
const endpoint = "https://nutwoodauto.group/query/json_simple"
const iext = '.jpg'
const iendpoint = "https://nutwoodauto.group/static/img/"
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

            // dimension items
            var mheight = data.height_in[i] + '"';
            var mwidth = data.width_in[i] + '"';
            var mlength = data.length_in[i] + '"';
            var mwheelbase = data.wheelbase[i] + '"';
            var mweight = data.curb_weight[i] + 'lbs';

            // generate the favorite list item
            var favorite_id = 'favid_' + data.manufacturer[i].toLowerCase() + '_' + (data.car_id[i]);
            var favorite_expand_id = 'favorite_expand_id_' + data.manufacturer[i].toLowerCase() + '_' + (i + 1);
            var favorite_box_id = 'favorite_box_id_' + data.manufacturer[i].toLowerCase() + '_' + (i + 1);
            var expand_favorite_span_id = 'expand_favorite_span_id_' + data.manufacturer[i].toLowerCase() + '_' + (i + 1);
            var favorite = `
            <div id="${favorite_box_id}" class="favorite_box">
              <li class="favorite" id="${favorite_id}"><span class="material-icons-round">favorite</span> ${text}</li>
              <button class="expand_close_favorite nue_expand_close_favorite" onclick="expand_close_favorite(${favorite_expand_id}, ${favorite_box_id}, ${expand_favorite_span_id})" type="button"><span id="${expand_favorite_span_id}" class="material-icons-round expand_favorite_span">expand_more</span></button>
            </div>
            <div id="${favorite_expand_id}" class="expanded_favorite_wrapper">
              <div class="expanded_favorite_wrapper_elements">
                <ul class="expand_list">
                  <li class="expanded_spec"><span class="material-icons-round">square_foot</span> Width: ${mwidth}</li>
                  <li class="expanded_spec"><span class="material-icons-round">square_foot</span> Height: ${mheight}</li>
                  <li class="expanded_spec"><span class="material-icons-round">square_foot</span> Length: ${mlength}</li>
                  <li class="expanded_spec"><span class="material-icons-round">square_foot</span> Wheelbase: ${mwheelbase}</li>
                  <li class="expanded_spec"><span class="material-icons-round">drive_eta</span> Curb Weight: ${mweight}</li>
                </ul>
              </div>
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

var expanded = 0;
var last_id;

function expand_close_favorite(id, fid, sid) {
  if (expanded == 0 ) {
    $(sid).html("expand_less");
    $(fid).css({"border-radius":"12px 12px 0 0"})
    $(id).slideDown(300);
    
    last_id = id;
    expanded = 1;
  } else {
    $(id).slideUp(300);
    $(sid).html("expand_more");
    setTimeout(() => {  $(fid).css({"border-radius":"12px"}); }, 200);

    last_id = id;
    expanded = 0;
  }
}