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
    document.getElementById('code').value = editor.getValue();
}
