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
    }else{
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
    }else{
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