

const navbarListDown = (element) => {
    console.log(element.parentElement)
    element.parentElement.querySelector("#icon-down-nav").style.display="none"
    element.parentElement.querySelector("#icon-up-nav").style.display="block"
    element.parentElement.parentElement.querySelector('.product-category-item-list').style.display='block'
}

const navbarListUp = (element) => {
     element.parentElement.querySelector("#icon-down-nav").style.display="block"
    element.parentElement.querySelector("#icon-up-nav").style.display="none"
    element.parentElement.parentElement.querySelector('.product-category-item-list').style.display='none'
}