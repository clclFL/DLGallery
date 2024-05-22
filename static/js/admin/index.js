const text = "Logging in as an administrator allows you to have the ability to view and manage website resources, while also being able to visually detect user behavior and traffic. Or just found this by chance? Don't be shy if you wanna apply for website admin, check the button below!";
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

