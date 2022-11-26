let editor = ace.edit("editor");
editor.setOptions({
    enableBasicAutocompletion: true,
    enableSnippets: true,
//    enableLiveAutocompletion: true
});

if (window.matchMedia('only screen and (max-width: 539px)')) {
    editor.setFontSize(18);
    editor.setOptions({
        wrap: true,
        indentedSoftWrap: false,
    });
}
else editor.setFontSize(22);

// https://cdnjs.com/libraries/ace/
ace.config.set('basePath','https://cdnjs.cloudflare.com/ajax/libs/ace/1.9.6');
editor.getSession().setMode("ace/mode/python");
editor.setTheme('ace/theme/chrome')

form = document.getElementById('submit');
function onFormSubmit() {
    try {
        if(form.submitted == 'T') {
            document.getElementById('form_button').style = 'display: none;';
            document.getElementById('test_data').style = '';
            return false;
        }

        document.getElementById('code').value = editor.getValue();
        return true;
    } catch (e) {
        alert('Error occurred: ' + e);
        console.log(e);
        return false;
    }
}

// disable bfcache
window.onpageshow = function(event) {
    if (event.persisted) {
        window.location.reload()
    }
};
