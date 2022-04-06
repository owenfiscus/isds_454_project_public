// consts
const endpoint = "https://nutwoodauto.group/query/json"
const iext = '.jpg'
const iendpoint = "https://static.nutwoodauto.group/img/"
const cards = document.getElementById('cards');

// vars
var arg = "?manu=";
var r = "?r="
var card_count = 0;

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

// remels function removes created cards
function rmels(parent){
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
  }
}

// handle enter key
$('#navForm').keypress(function(event){
  var keycode = (event.keyCode ? event.keyCode : event.which);
  if(keycode == '13'){
      // stop page reload on enter
      event.preventDefault();
      $("#openBtn").trigger("click");
  }
});

// qcall function for search
window.onload = function() {
    // remove previously created cards
    rmels(document.getElementById("cards"));

    var json_url = localStorage.getItem('nutwood_search_url');
    // getting pictures for the cars and displaying in html
    getdata(json_url)
        .then(function(result) {
          var data = JSON.parse(result);
          var count = Object.keys(data.car_id).length;
          for (let i = 0; i < count; i++) {
            // form the path to the images
            var imgurl = iendpoint + data.manufacturer[i].toLowerCase() + '_' + data.car_id[i] + iext;
            // get the name of the vehicle
            var text = data.manufacturer[i] + " " + data.model[i] + " " + data.trim_[i];

            var xhr = new XMLHttpRequest();
            xhr.open('HEAD', imgurl, false);
            xhr.send();
            if (xhr.status == 404) {
              imgurl = iendpoint + "fallback.png"
            }

            // create image elements
            var img = document.createElement('img');
            img.id = 'image' + i;
            img.class = 'image';
            img.src = imgurl;

            var mimg = document.createElement('img');
            mimg.id = 'mimage' + i;
            mimg.class = 'mimage';
            mimg.src = imgurl;
            
            
            // generate the card element
            var imgid = 'img' + i;
            var textid = 'txt' + i;
            var pid = 'p' + i;
            var bid = 'b' + '_' + data.manufacturer[i].toLowerCase() + '_' + data.car_id[i];
            var cardid = data.manufacturer[i].toLowerCase() + '_' + data.car_id[i];
            var hid = "heart_" + data.manufacturer[i].toLowerCase() + '_' + data.car_id[i];
            var card = `<div class="card nuecard" id="${cardid}">
                          <div class="cimgwrp" id="${imgid}"></div>
                          <div class="ctext" id="${textid}">
                            <p id="${pid}"></p>
                            <span id="${hid}" class="material-icons-round heart">favorite</span>
                          </div>
                          <button id="${bid}" class="morebtn nuemorebtn" type="button" ><span class="material-icons-round">add</span></button>
                        </div>`;

            // add the card element to html
            cards.insertAdjacentHTML('beforeend', card);
            
            // add the img element to the card
            cardelement = document.getElementById(imgid);
            cardelement.appendChild(img);

            // add the ctext element to the card
            p = document.getElementById(pid);
            // add text to the card
            p.appendChild(document.createTextNode(text));

            // generate the modal element
            // general modal items
            var mimgid = 'mimg' + i;
            var mvdmid = 'mvdm' + i;
            var mtextid = 'mtxt' + i;
            var mpid = 'mp' + i;
            var mbid = 'mbid_' + data.manufacturer[i].toLowerCase() + '_' + (i + 1) ;
            var favid = 'favid_' + data.manufacturer[i].toLowerCase() + '_' + (i + 1);
            var smbid = 'smbid_' + data.manufacturer[i].toLowerCase() + '_' + (i + 1);
            var modalid = 'modal_' + data.manufacturer[i].toLowerCase() + '_' + data.car_id[i];
            var hmdid = 'hmd_' + data.manufacturer[i].toLowerCase() + '_' + data.car_id[i];
            var manulink = data.web_link[i];

            // modal table items
            var mprice = '$' + data.msrp_price[i];
            var fuelecon = data.city_mpg[i] + ' / ' + data.highway_mpg[i];
            var engval = data.engine[i];
            var transval = data.transmission_type[i];
            var dtval = data.drivetrain_type[i];

            // dimension items
            var mheight = data.height_in[i] + '"';
            var mwidth = data.width_in[i] + '"';
            var mlength = data.length_in[i] + '"';
            var mwheelbase = data.wheelbase[i] + '"';
            var mweight = data.curb_weight[i] + 'lbs';
            
            var modal = `
                        <div class="modal nuemodal" id="${modalid}" style="display: none;">
                          <button id="${mbid}" class="closebtn nueclosebtn" onclick="closemodal()" type="button" ><span class="material-icons-round">close</span></button>
                          <button id="${favid}" class="favbtn nuefavbtn" onclick="favorite_vehicle('${favid}', '${data.manufacturer[i]}', '${data.model[i]}', '${data.car_id[i]}', '${hid}')" type="button" ><span class="material-icons-round">favorite</span></button>
                          <div class="mimgwrp" id="${mimgid}" onclick="showimg('${mimgid}', '${imgurl}', '${modalid}')"></div>
                          <div class="m_v_dimensions" id="${mvdmid}">
                          <div class="mrow"><p class="mspec"><span class="material-icons-round">square_foot</span> Height: </p><p class="mval">${mheight}</p></div>
                          <div class="mrow"><p class="mspec"><span class="material-icons-round">square_foot</span> Width: </p><p class="mval">${mwidth}</p></div>
                          <div class="mrow"><p class="mspec"><span class="material-icons-round">square_foot</span> Length: </p><p class="mval">${mlength}</p></div>
                          <div class="mrow"><p class="mspec"><span class="material-icons-round">square_foot</span> Wheelbase: </p><p class="mval">${mwheelbase}</p></div>
                          <div class="mrow"><p class="mspec"><span class="material-icons-round">drive_eta</span> Curb Weight: </p><p class="mval">${mweight}</p></div>
                          </div>
                          <div class="modal_title"><p id="${mpid}">${text}</p></div>
                          <div class="mtext" id="${mtextid}">
                            <div class="modal_detail">
                                <div class="mrow"><p class="mspec"><span class="material-icons-round">savings</span> MSRP: </p><p class="mval">${mprice}</p></div>
                                <div class="mrow"><p class="mspec"><span class="material-icons-round">local_gas_station</span> Fuel Economy: </p><p class="mval">${fuelecon} MPG</p></div>
                            </div>
                            <button id="${smbid}" onclick="mshowm(${hmdid}, ${smbid})" class="modal_show_more_btn" type="button">Show more</button>
                            <div class="h_modal_detail" id="${hmdid}">
                                <div class="mrow"><p class="mspec"><span class="material-icons-round">settings</span> Engine: </p><p class="mval">${engval}</p></div>
                                <div class="mrow"><p class="mspec"><span class="material-icons-round">settings</span> Transmission: </p><p class="mval">${transval}</p></div>
                                <div class="mrow"><p class="mspec"><span class="material-icons-round">settings</span> Drive Train: </p><p class="mval">${dtval}</p></div>
                            </div>
                          </div>
                          <div class="modal_manu_link"><a href="${manulink}">Manufacturer Website <span class="material-icons-round">launch</span></p></div>
                        </div>`;

            // add the modal element to html
            cards.insertAdjacentHTML('beforeend', modal);
            mimgelement = document.getElementById(mimgid);
            mimgelement.appendChild(mimg);
            var local_id = favid.toString();
            var local_data = JSON.parse(localStorage.getItem(local_id));
            // only perform the check if the data is available
            if (local_data != null || undefined && local_data.set == 1) {
              $('#' + favid).addClass('favorited');
              $('#' + hid).css("visibility", "visible");
            }
            // count the number of cards on the page
            card_count = $('.card').length;
          }
          // display placeholder text if no cards are loaded
          if (card_count == 0) {
            $('#placeholder').fadeIn(200);
          }
        })
    }

const onClick = (event) => {
  var id = event.target.id;

  if (id.startsWith('b')) {
    id = "#modal" + id.substring(1, id.length)
    $('#page-mask').fadeIn(200);
    $(id).fadeIn(200);
    window.scrollTo(0, 0);
  }
}

window.addEventListener('click', onClick);

function closemodal() {
  $('#page-mask').fadeOut(200);
  $('.modal').fadeOut(200);
}

var smstate = 1;

function mshowm(id, btnid) {
  if (smstate == 1) {
    $(id).fadeIn(200);
    btnid.textContent = "Show less";
    smstate = 2;
  } else {
    $(id).fadeOut(200);
    btnid.textContent = "Show more";
    smstate = 1;
  }
}

function showimg(id ,url, modalid) {
  var m = modalid;
  var large_img_id = "large_" + id;
  var close_large_img_id = "close_large_" + id;
  var large_img_modal = `
                        <div class="large_img_modal" id="${large_img_id}">
                          <div class="large_img_wrap">
                            <div class="large_img_btn_bg"><button id="${close_large_img_id}" class="closebtn nueclosebtn large_img_close" onclick="closeimage(${m})" type="button" ><span class="material-icons-round">close</span></button></div>
                            <img src="${url}"></img>
                          </div>
                        </div>`

  cards.insertAdjacentHTML('beforeend', large_img_modal);
  $('#' + m).css("visibility", "hidden");
  $(".large_img_modal").fadeIn(200);
}

function closeimage(m) {
  $(".large_img_modal").fadeOut(200);
  // remove the image modal after the fadeout
  $(m).css("visibility", "visible");
  setTimeout(() => {  $(".large_img_modal").remove(); }, 200);
}

function favorite_vehicle(id, manufacturer, model, car_id, hid) {
  var faved = JSON.parse(localStorage.getItem(id));
  if (faved != null || undefined && faved.set == 1) {
    $('#' + id).removeClass('favorited');
    $('#' + hid).css("visibility", "hidden");
    localStorage.setItem(id , null);
  } else {
    $('#' + id).addClass('favorited');
    $('#' + hid).css("visibility", "visible");
    stored_data = {'set': 1, 'manufacturer': manufacturer, 'model': model, 'car_id': car_id};
    localStorage.setItem(id , JSON.stringify(stored_data));
  }
}