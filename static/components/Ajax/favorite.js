


const addFavorite = (id) => {
    $.ajax({
        url: `/product/favorite/${id}`,
        data: {},
        dataType: 'html',
        success: (data) => {
            $(`.favorite-false-${id}`).css("display", "none")
            $(`.favorite-true-${id}`).css("display", "block")
        }
    })
}


const removeFavorite = (id) => {
    $.ajax({
        url: `/product/favorite/${id}`,
        data: {},
        dataType: 'html',
        success: (data) => {
            $(`.favorite-false-${id}`).css("display", "block")
            $(`.favorite-true-${id}`).css("display", "none")
        }
    })
}

const removeFavoriteInList = (id) => {
    $.ajax({
        url: `/product/favorite/${id}`,
        data: {},
        dataType: 'html',
        success: (data) => {
            $('#favourite_list').html(data);
        }
    })
}