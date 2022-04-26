const base_url= "https://nutwoodauto.group/analytics_result"

var drop_down_1 = document.getElementById('analytics_drop_down_1');
var drop_down_2 = document.getElementById('analytics_drop_down_2');
var drop_down_3 = document.getElementById('analytics_drop_down_3');
var drop_down_4 = document.getElementById('analytics_drop_down_4');

var checkbox_1 = document.getElementById('analytics_checkbox_1');
var checkbox_2 = document.getElementById('analytics_checkbox_2');
var checkbox_3 = document.getElementById('analytics_checkbox_3');
var checkbox_4 = document.getElementById('analytics_checkbox_4');

function generate_analytics() {
    var arg_string = '';

    var manu1 = drop_down_1.value;
    var manu2 = drop_down_2.value;
    var drivetrain = drop_down_3.value;
    var transmission = drop_down_4.value;

    var msrp = document.querySelector('#analytics_checkbox_1').checked;
    var fuel_tank_size = document.querySelector('#analytics_checkbox_2').checked;
    var mpg = document.querySelector('#analytics_checkbox_3').checked;
    var horsepower = document.querySelector('#analytics_checkbox_4').checked;

    // catch case where two brands are not selected
    if (manu1 == '' || manu2 == '') {
        $('#analytics_error_text').html('⚠️ You must choose two brands!');
        $('#analytics_error').fadeIn(200);
    } else if (manu1 == manu2) {
        $('#analytics_error_text').html('⚠️ You must choose different brands!');
        $('#analytics_error').fadeIn(200);
    } else if (msrp == false && fuel_tank_size == false && mpg == false && horsepower == false) {
        $('#analytics_error_text').html('⚠️ You must select at least one checkbox!');
        $('#analytics_error').fadeIn(200);
    } else {
        arg_string = arg_string.concat(`?manu1=${manu1}&manu2=${manu2}`);
        var open_url = true;
    }



    // check if options are selected
    if (drivetrain != '') {
        arg_string = arg_string.concat(`&drivetrain=${drivetrain}`);
    }
    
    if (transmission != '') {
        arg_string = arg_string.concat(`&transmission=${transmission}`);
    }
    
    if (msrp != '') {
        arg_string = arg_string.concat(`&msrp=${msrp}`);
    }

    if (fuel_tank_size != '') {
        arg_string = arg_string.concat(`&fuel_tank_size=${fuel_tank_size}`);
    }

    if (mpg != '') {
        arg_string = arg_string.concat(`&mpg=${mpg}`);
    }

    if (horsepower != '') {
        arg_string = arg_string.concat(`&horsepower=${horsepower}`);
    }

    // only open the page if the search meets minimum requirements
    if (open_url == true) {
        // combine base url and arg string
        let analytics_url = `${base_url}${arg_string}`;
        // open page
        window.location.href = analytics_url;
    }
}

// reset dropdowns, checkboxes, error messages when returned to page with back button
window.addEventListener("pageshow", () => {
    // hide error message
    $('#analytics_error').css("display", "none");

    // set dropdown index to 0
    drop_down_1.selectedIndex = 0;
    drop_down_2.selectedIndex = 0;
    drop_down_3.selectedIndex = 0;
    drop_down_4.selectedIndex = 0;

    // uncheck checkboxes
    checkbox_1.checked = false;
    checkbox_2.checked = false;
    checkbox_3.checked = false;
    checkbox_4.checked = false;
  });
