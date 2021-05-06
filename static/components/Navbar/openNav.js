
const openNav = () => {
    document.querySelector('.nav-menu').style.display = "block"
}

const closeNav = () => {
    setTimeout(() => document.querySelector('.nav-menu').style.display = "none", 400)
}