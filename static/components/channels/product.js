$(function () {
    const endpoint = 'ws://127.0.0.1:8000/ws/products/'
    const socket = new WebSocket(endpoint)

    socket.onopen = function (e) {
        console.log("open", e);
    }
    socket.onmessage = function (e) {
        console.log("message", e)
        const data = JSON.parse(e.data);
        console.log(data)

    }
    socket.onerror = function (e) {
        console.log("error", e)
    }
    socket.onclose = function (e) {
        console.log("close", e)
    }
});
