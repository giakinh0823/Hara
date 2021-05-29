


const submitFormCreate = (e) => {
    e.preventDefault();
    $.ajax({
        url: '',
        type: 'post',
        data: new FormData(document.getElementById("create-product")),
        processData: false,
        contentType: false,
        dataType: 'html',
        success: function (data){
            $("#create-product")[0].reset()
            $("#create-product-preview").html(data)
        }
    })
}

