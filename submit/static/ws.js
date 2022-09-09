const socket = new WebSocket(location.protocol == 'https:'?'wss://':'ws://' + window.location.host + '/submit/ws');
const result = document.getElementById('result');

socket.onmessage = function(e) {
    let data = JSON.parse(e.data)
    console.log(data)

    switch(data['type']) {
        case 'progress':
            result.innerHTML = '🔁 진행 중 (' +  parseInt(data['progress']) + '%)'
            break;
        case 'reload':
            location.reload();
            break;
        default:
            console.error(data)
    }
}

waiting = []

function register(submit_id) {
    if(socket.readyState === 1) {
        socket.send(JSON.stringify({
            'register': submit_id
        }))
    } else {
        waiting.push(submit_id);
    }
}

socket.onopen = function() {
    for(let submit_id of waiting) {
        register(submit_id);
    }
    waiting = [];
}
