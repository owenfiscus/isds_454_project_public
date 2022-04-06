// dark mode script / saves state to browser local storage
(function() {
    let onpageLoad = localStorage.getItem("theme") || "";
    let element = document.body;
    if (onpageLoad != "") { element.classList.add(onpageLoad); }
})();

function light_dark() {
    var element = document.body;
    element.classList.toggle("darkMode");

    let theme = localStorage.getItem("theme");
    if (theme && theme === "darkMode") {
        localStorage.setItem("theme", "");
    } else {
        localStorage.setItem("theme", "darkMode");
    }
}
