


const clearNotifyMessage = () => {
    $.ajax({
        url:'',
        data: {},
        dataType: 'json',
        success: (data) => {
            console.log(data.success)
        }
    })
}