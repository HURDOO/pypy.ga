let editor = ace.edit("editor");
editor.setOptions({
    enableBasicAutocompletion: true,
    enableSnippets: true,
    enableLiveAutocompletion: true
})
editor.setFontSize(20);
editor.getSession().setMode("ace/mode/python");
