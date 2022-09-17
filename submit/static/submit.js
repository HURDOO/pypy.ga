const params = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
})

document.getElementById('submit_id').value = params['submit_id']
document.getElementById('user_id').value = params['user_id']
