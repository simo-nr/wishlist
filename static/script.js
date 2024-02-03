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

function checkOffItem(itemId, button) {
    fetch(`/checkoff/${itemId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // include additional info later
        body: JSON.stringify({}),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        button.disabled = true;
        return response.json();
    })
    .then(data => {
        // Handle the response from the server if needed
        console.log(data);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}