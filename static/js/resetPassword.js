const text = "Meet with problem that cannot be solved? Please don't mind sending me a feedback, Personal Email: pineclone@outlook.com";
let index = 0;

function printText() {
    document.getElementById('text').textContent += text[index];
    index++;
    if (index < text.length) {
        setTimeout(printText, 35); // 设置文本显示速度
    }
}

printText();

function toggleVisibility() {
    var passwordField = document.getElementById("password");
    var visibilityIcon = document.getElementById('visibilityIcon')
    if (passwordField.type === "password") {
        visibilityIcon.classList.remove('glyphicon-eye-close')
        visibilityIcon.classList.add('glyphicon-eye-open')
        passwordField.type = "text";
    } else {
        visibilityIcon.classList.remove('glyphicon-eye-open')
        visibilityIcon.classList.add('glyphicon-eye-close')
        passwordField.type = "password";
    }
}
