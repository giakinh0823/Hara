const submitFormImageAndVideo = (e, id) => {
    if (id === 0) {
        e.preventDefault();
        $.ajax({
            url: '',
            type: 'post',
            data: new FormData(document.getElementById(`info-product-form-${id}`)),
            processData: false,
            contentType: false,
            dataType: 'html',
            success: function (data) {
                console.log(document.getElementById(`info-product-form-${id}`))
                $("#info-product-preview").html(data)
            }
        })
    } else {
        e.preventDefault();
        $.ajax({
            url: `newInfoImage/${id}/`,
            type: 'post',
            data: new FormData(document.getElementById(`info-product-form-${id}`)),
            processData: false,
            contentType: false,
            dataType: 'html',
            success: function (data) {
                console.log(document.getElementById(`info-product-form-${id}`))
                $("#info-product-preview").html(data)
                $(`#button-edit-image-${id}`).css("display", "block")
                $(`.input-edit-image-${id}`).css("display", "none")
            }
        })
    }
}


const submitFormVideo = (e, id) => {
    if (id === 0) {
        e.preventDefault();
        $.ajax({
            url: '',
            type: 'post',
            data: new FormData(document.getElementById(`info-product-video-${id}`)),
            processData: false,
            contentType: false,
            dataType: 'html',
            success: function (data) {
                $("#info-product-preview").html(data)
            }
        })
    } else {
        e.preventDefault();
        $.ajax({
            url: `newvideo/${id}/`,
            type: 'post',
            data: new FormData(document.getElementById(`info-product-video-${id}`)),
            processData: false,
            contentType: false,
            dataType: 'html',
            success: function (data) {
                console.log(document.getElementById(`info-product-video-${id}`))
                $("#info-product-preview").html(data)
            }
        })
    }
}

const editImage = (id) => {
    $(`#button-edit-image-${id}`).css("display", "none")
    $(`.input-edit-image-${id}`).css("display", "block")
}


const deleteVideo = (id) => {
    console.log(window.location)
    $.ajax({
        url: window.location.pathname+`deleteVideo/${id}/`,
        data: {"id": id},
        dataType: 'html',
        success: function (data) {
            $('#list_video_product').html(data)
        }
    })
}

const deleteImage = (id) => {
    console.log(window.location)
    $.ajax({
        url: window.location.pathname+`deleteImage/${id}/`,
        data: {"id": id},
        dataType: 'html',
        success: function (data) {
            $('#list_image_product').html(data)
        }
    })
}