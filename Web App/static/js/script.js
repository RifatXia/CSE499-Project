// let menubar = document.querySelector("#menu-bar")
// let mynav = document.querySelector(".navbar")

// menubar.onclick = () => {
//     menubar.classList.toggle('fa-times')
//     mynav.classList.toggle("active")
// }
function showContent(contentType) {
    // Hide all content divs
    var contents = document.getElementsByClassName('content');
    for (var i = 0; i < contents.length; i++) {
        contents[i].style.display = 'none';
    }

    // Show the selected content
    document.getElementById(contentType + 'Content').style.display = 'block';
}

