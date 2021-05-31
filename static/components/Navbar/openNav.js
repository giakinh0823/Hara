const openNav = () => {
    document.querySelector('.nav-menu').style.display = "block"
}

const closeNav = () => {
    setTimeout(() => document.querySelector('.nav-menu').style.display = "none", 400)
}

if (document.querySelector('.nav-menu-content-responsive').style.display === "flex") {
        document.querySelector('#button-nav-menu-open').style.display = "none"
        document.querySelector('#button-nav-menu-close').style.display = "block"
    } else {
        document.querySelector('#button-nav-menu-open').style.display = "block"
        document.querySelector('#button-nav-menu-close').style.display = "none"
        document.querySelector('.nav-menu-content-responsive')
    }

const openNavMenu = () => {
    document.querySelector('.nav-menu-content-responsive').style.display = "flex"
    document.querySelector('#button-nav-menu-open').style.display = "none"
    document.querySelector('#button-nav-menu-close').style.display = "block"

}

const closeNavMenu = () => {
    document.querySelector('.nav-menu-content-responsive').style.display = "none"
    document.querySelector('#button-nav-menu-close').style.display = "block"
    document.querySelector('#button-nav-menu-open').style.display = "block"
    document.querySelector('#button-nav-menu-close').style.display = "none"
}

$('.body-container').mouseup(closeNavMenu)
