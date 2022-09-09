const socket = new WebSocket('ws://' + window.location.host + '/submit/ws')

socket.onmessage = function(e) {
    console.log(e.data)
}

function register(submit_id) {
    socket.send(JSON.stringify({
        'register': submit_id
    }))
}

document.getElementById('send').onclick = function(e) {
    register(document.getElementById('submit_id').value)
}
