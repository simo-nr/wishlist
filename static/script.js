function toggleMenu() {
    console.log("button is clicked");
    var menu = document.getElementById('menu');
    var content = document.getElementById('content');
    var menuIcon = document.getElementById('menu-icon');

    if (menu.style.left === "0px") {
        menu.style.left = "-250px";
        content.style.marginLeft = "0";
    } else {
        menu.style.left = "0px";
        content.style.marginLeft = "250px";
    }
    console.log("function worked");
}

function closeMenu() {
    var menu = document.getElementById('menu');
    var content = document.getElementById('content');
    var menuIcon = document.getElementById('menu-icon');

    menu.style.left = "-250px";
    content.style.marginLeft = "0";
}