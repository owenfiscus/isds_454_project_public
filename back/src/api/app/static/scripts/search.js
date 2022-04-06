// define variables & constants
var drop_down_1 = document.getElementById('drop_down_1');
var drop_down_2 = document.getElementById('drop_down_2');

var price_values = {};
var horsepower_values = {};
var mpg_values = {};

// base url
const base_url = "https://nutwoodauto.group";

// endpoints
const endpoint = `${base_url}/query/json?`;
const models_endpoint = `${base_url}/query/models_json?`;
const all_json_endpoint = `${base_url}/query/all_json?`;

function search() {
    var arg_string = '';
    var values_string = `&price_min=${price_values.min}&price_max=${price_values.max}&hp_min=${horsepower_values.min}&hp_max=${horsepower_values.max}&mpg_min=${mpg_values.min}&mpg_max=${mpg_values.max}`;

    if (drop_down_1 != null || undefined || '' &&
        drop_down_1.value != null || undefined || '') {
            arg_string = arg_string.concat(`manu=${drop_down_1.value}`);
    }

    if (drop_down_2 != null || undefined || ''  &&
        drop_down_2.value != null || undefined || '') {
            arg_string = arg_string.concat(`&`);
            arg_string = arg_string.concat(`model=${drop_down_2.value}`);
    }

    if (drop_down_1.value === '' &&
        drop_down_2.value === '') {
            localStorage.setItem('nutwood_search_url', all_json_endpoint + values_string);
            window.location.href = `${base_url}/cards`;
        } else {
            localStorage.setItem('nutwood_search_url', endpoint + arg_string + values_string);
            window.location.href = `${base_url}/cards`;
        }
}

// populate models on option selection
drop_down_1.onchange = function() {
    remove_elements(drop_down_2);
    // call populate models function with the selected make
    populate_models(drop_down_1.value);
    // reset the model index to the placeholder text
    drop_down_2.selectedIndex = 0;
}

// pull model data and create options
function populate_models(make) {
    remove_elements(drop_down_2);

    make_request(models_endpoint + 'manu=' + make)
    .then(function(result) {
        var data = JSON.parse(result);
        var count = Object.keys(data.model).length;
        
        // add the default option
        drop_down_2.insertAdjacentHTML('afterbegin', `<option value="" disabled selected>Model</option>`);

        // add model options
        for (let i = 0; i < count; i++) {
            var option = `<option class="model_option" value="${data.model[i]}">${data.model[i]}</option>`;
            drop_down_2.insertAdjacentHTML('beforeend', option);
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

// remove created options
function remove_elements(parent){
    while (parent.children.length) {
        parent.removeChild(parent.firstChild);
    }
}

// sliders
function get_slider_values(){
    // get slider values
    var parent = this.parentNode;
    var slides = parent.getElementsByTagName("input");
    var slide1 = parseFloat( slides[0].value );
    var slide2 = parseFloat( slides[1].value );

    switch (parent) {
      case document.getElementById('range_slider_price'):
        price_values = {
          "min" : slide1,
          "max" : slide2
        }
        break;
      case document.getElementById('range_slider_horsepower'):
        horsepower_values = {
          "min" : slide1,
          "max" : slide2
        }
        break;
      default:
        mpg_values = {
          "min" : slide1,
          "max" : slide2
        }
    }

    // neither slider will clip the other, determine which is larger
    if( slide1 > slide2 ){ var tmp = slide2; slide2 = slide1; slide1 = tmp; }
    
    var displayElement = parent.getElementsByClassName("range_values")[0];
        displayElement.innerHTML = slide1 + " - " + slide2;
  }
  
  window.onload = function(){
    // initialize sliders
    var sliderSections = document.getElementsByClassName("range_slider");
        for( var x = 0; x < sliderSections.length; x++ ){
          var sliders = sliderSections[x].getElementsByTagName("input");
          for( var y = 0; y < sliders.length; y++ ){
            if( sliders[y].type ==="range" ){
              sliders[y].oninput = get_slider_values;
              // manually trigger event first time to display values
              sliders[y].oninput();
            }
          }
        }
  }
