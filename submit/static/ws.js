const socket = new WebSocket('ws://' + window.location.host + '/submit/ws')

socket.onmessage = function(e) {
    console.log(e.data)
}

document.getElementById('send').onclick = function(e) {
    socket.send('test')
}
