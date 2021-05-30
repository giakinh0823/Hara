


const addFavorite = (id) => {
    $.ajax({
        url: `/product/favorite/${id}`,
        data: {},
        dataType: 'json',
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
        dataType: 'json',
        success: (data) => {
            $(`.favorite-false-${id}`).css("display", "block")
            $(`.favorite-true-${id}`).css("display", "none")
        }
    })
}