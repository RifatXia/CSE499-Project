let menubar = document.querySelector("#menu-bar")
let mynav = document.querySelector(".navbar")

menubar.onclick = () => {
    menubar.classList.toggle('fa-times')
    mynav.classList.toggle("active")
}
