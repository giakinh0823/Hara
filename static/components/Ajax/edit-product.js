


const submitFormEdit = (e) => {
    e.preventDefault();
    $.ajax({
        url: '',
        type: 'post',
        data: new FormData(document.getElementById("edit-product-form")),
        processData: false,
        contentType: false,
        dataType: 'html',
        success: function (data){
            console.log(document.getElementById("edit-product-form"))
            $("#edit-product-preview").html(data)
        }
    })
}