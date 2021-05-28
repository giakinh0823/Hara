

const sortProduct = (value) => {
    console.log(window.location)
    let href = window.location.href
    console.log(href);
    $.ajax({
        url: href.toString(),
        data: {"value": value},
        dataType: 'html',
        success: function (data, textStatus, jqXHR) {
            $('#list-product-container').html(data);
        }
    })
}


const sort = (value) => {
    if (value > 0) {
        sortProduct(value);
    }
}
