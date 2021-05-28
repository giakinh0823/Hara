const activeOrder = (id) => {
    $.ajax({
        url: 'active',
        data: {"id": id},
        success: (data) => {
            clearTimeout();
            $('#toast-order-active').css("display", "block");
            $('#toast-body-text').text(`Product is active`)
            setTimeout(() => {
                $('#toast-order-active').css("display", "none");
            }, 3000)
        }
    })
}

const closeOrderActive = () => {
    clearTimeout();
    $('#toast-order-active').css("display", "none");
}

const orderSuccess = (id) => {
    $.ajax({
        url: 'success',
        data: {"id": id},
        success: async (data) => {
            clearTimeout();
            const status = "đã hoàn thành"
            await sendNotify(data.user, data.person, data.product, data.link, status).then(r => {
                $('#toast-body-text').text(`${data.text} Has been updated`)
                $('#toast-order-active').css("display", "block");
                $(`#order-status-${id}`).removeClass().addClass('success').text("Success");
            })
            setTimeout(() => {
                $('#toast-order-active').css("display", "none");
            }, 3000)
        }
    })
}


const orderCancel = (id) => {
    $.ajax({
        url: 'cancel',
        data: {"id": id},
        success: async (data) => {
            clearTimeout();
            const status = "đã hủy sản phẩm"
            await sendNotify(data.user, data.person, data.product, data.link, status).then(r => {
                $('#toast-body-text').text(`${data.text} Has been cancel`)
                $('#toast-order-active').css("display", "block");
                $(`#order-status-${id}`).removeClass().addClass('cancel').text("Cancel");
            })
            setTimeout(() => {
                $('#toast-order-active').css("display", "none");
            }, 3000)
        }
    })
}

const orderAccept = (id) => {
    $.ajax({
        url: 'accept',
        data: {"id": id},
        success: async (data) => {
            clearTimeout();
            const status = "đã được xác nhận"
            await sendNotify(data.user, data.person, data.product, data.link, status).then(r => {
                $('#toast-body-text').text(`Has been accept`)
                $('#toast-order-active').css("display", "block");
                $(`#order-status-${id}`).removeClass().addClass('waiting').text("Waiting");
            })
            setTimeout(() => {
                $('#toast-order-active').css("display", "none");
            }, 3000)
        }
    })
}


const sendNotify = async (user, person, product, link, status) => {

    const endpointPerson = `ws://127.0.0.1:8000/ws/notify/${person}/`

    let promise = new Promise(async (resolve, reject) => {
        const socketPerson = await new WebSocket(endpointPerson)
        resolve(socketPerson)
    })

    promise.then(async (socketPerson) => {
        socketPerson.onopen = await function (e) {
            console.log("open", e);
        }
        setTimeout(() => {
            socketPerson.send(JSON.stringify({
                'comment': `Sản phẩm ${product} ${status}`,
                'username': `${person}`,
                'room': `${person}`,
                'link': `${link}`,
                'person': `${user}`,
            }));
        }, 1000)
        socketPerson.onerror = function (e) {
            console.log("error", e)
        }

        socketPerson.onclose = function (e) {
            console.log("close", e)
        }
    })
}