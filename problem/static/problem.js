let editor = ace.edit("editor");
editor.setOptions({
    enableBasicAutocompletion: true,
    enableSnippets: true,
    enableLiveAutocompletion: true
})
editor.setFontSize(20);
// https://cdnjs.com/libraries/ace/
ace.config.set('basePath','https://cdnjs.cloudflare.com/ajax/libs/ace/1.9.6');
editor.getSession().setMode("ace/mode/python");
editor.setTheme('ace/theme/chrome')

document.querySelector('form').onsubmit = (event) => {
    try {
        document.getElementById('code').value = editor.getValue();
        console.log(new Date().toISOString());
        document.getElementById('submit_time').value = new Date().toISOString();
        console.log(document.getElementById('submit_time').value)
        return true;
    } catch (e) {
        alert('Error occurred: ' + e);
        console.log(e);
        return false;
    }
}
