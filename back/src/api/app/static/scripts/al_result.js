var chart0 = document.getElementById('chart0');
var chart1 = document.getElementById('chart1');
var chart2 = document.getElementById('chart2');
var chart3 = document.getElementById('chart3');
var chart4 = document.getElementById('chart4');

var charts = [chart0, chart1, chart2, chart3, chart4];

window.onload = function(){ 
    // hide blank charts
    for (var i in charts) {
        if (charts[i].innerHTML == '') {
            $(charts[i]).parent().css('display', 'none');
        }
    }

    // wait for 2.5 seconds then call display analytics function
    setTimeout( () => display_analytics(), 2500);
}

function display_analytics() {
    // hide analytics placeholder
    $('#analytics_placeholder ').fadeOut(200);
    
    // show analytics
    $('#analytics_result').css('display', 'flex');
}
