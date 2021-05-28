


onInput = (element) => {
    element.parentNode.querySelector('.nav-search-btn').style.display = "none";
    element.parentNode.querySelector('.nav-close-btn').style.display = "block";
}

onBlur= (element) => {
    console.log(element)
    if (!element.value.trim()) {
        element.parentNode.querySelector('.nav-search-btn').style.display = "block";
        element.parentNode.querySelector('.nav-close-btn').style.display = "none";
    }
}

deleteInput = (element) => {
    console.log(element)
    element.parentNode.querySelector('.nav-search-input').value=''
    element.parentNode.querySelector('.nav-search-input').focus()
}