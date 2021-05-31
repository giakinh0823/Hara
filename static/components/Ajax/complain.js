


const submitFormComplain = (e) => {
    e.preventDefault();
    $(".loading-over").css("display","block")
    $.ajax({
        url: '',
        type: 'post',
        data: $("#form-complain").serialize(),
        dataType: 'json',
        success: async (data) => {
            setTimeout(() => {
                $(".loading-over").css("display","none")
                $("#complain-success").css("display","flex")
                $("#form-complain")[0].reset()
            }, 1500)
            setTimeout(() => {
                $("#complain-success").css("display","none")
            }, 4000)
        },
        error: () => {
            setTimeout(() => {
                $(".loading-over").css("display","none")
                $("#complain-error").css("display","flex")
            }, 1500)
            setTimeout(() => {
                $("#complain-error").css("display","none")
            }, 4000)
        }
    })
}