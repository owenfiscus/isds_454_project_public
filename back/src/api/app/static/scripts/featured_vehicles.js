// define constants
const random_json_endpoint = "https://nutwoodauto.group/query/random_json";

// define variables
var image_base_url = "https://static.nutwoodauto.group/img";
var image_extension = '.jpg';
var featured_slideshow = document.getElementById('featured_slideshow');
var featured_vehicles = document.getElementById('featured_vehicles');

// pull model data and create options
window.onload = function populate_images() {

    make_request(random_json_endpoint)
    .then(function(result) {
        var data = JSON.parse(result);
        var count = Object.keys(data.car_id).length;

        // add model options
        for (let i = 0; i < count; i++) {
            // create image variable
            var image_url = `${image_base_url}/${data.manufacturer[i].toLowerCase()}_${data.car_id[i]}${image_extension}`

            // use placeholder if image doesn't exist
            var xhr = new XMLHttpRequest();
            xhr.open('HEAD', image_url, false);
            xhr.send();
            if (xhr.status == 404) {
              image_url = "https://static.nutwoodauto.group/img/fallback.png"
            }

            var label = `${data.manufacturer[i]} ${data.model[i]} ${data.trim_[i]}`;

            var image = `<img class="slideshow_image" src="${image_url}"></img>`;
            var image_label = `<div class="image_label">${label}</div>`;

            featured_vehicles.insertAdjacentHTML('beforeend', image_label);
            featured_slideshow.insertAdjacentHTML('beforeend', image);
        }

        // automatic slideshow logic
        let slide_index = 0;
        let label_index = 0;
        show_slides();
        
        function show_slides() {
          let i;
          let slides = document.getElementsByClassName("slideshow_image");
          let labels = document.getElementsByClassName("image_label");
          
          for (i = 0; i < slides.length; i++) {
            $(slides[i]).fadeOut(0);
          }

          for (i = 0; i < labels.length; i++) {
            $(labels[i]).fadeOut(0);
          }

          slide_index++;
          label_index++;

          if (slide_index > slides.length) {slide_index = 1}
          if (label_index > labels.length) {label_index = 1}

          $(slides[slide_index-1]).fadeIn(500); // .5s
          $(labels[slide_index-1]).fadeIn(500); // .5s
          setTimeout(show_slides, 5000); // 5s
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
