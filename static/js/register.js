const text = "Register as a user for the visiting access";
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

function sendEmail() {
    let email = $('#email').val();

    var cooldownTime = 30; // 冷却时间，以秒为单位
    var cooldownInterval; // 定时器

    // 禁用按钮
    document.getElementById("sendButton").disabled = true;

    // 更新按钮文本为剩余时间
    document.getElementById("sendButton").textContent = "Verify Email (" + cooldownTime + "s)";

    // 设置定时器每秒更新剩余时间
    cooldownInterval = setInterval(function () {
        cooldownTime--;
        if (cooldownTime > 0) {
            document.getElementById("sendButton").textContent = "Verify Email (" + cooldownTime + "s)";
        } else {
            // 取消定时器并重新启用按钮
            clearInterval(cooldownInterval);
            document.getElementById("sendButton").textContent = "Verify Email";
            document.getElementById("sendButton").disabled = false;
            cooldownTime = 30; // 重置冷却时间
        }
    }, 1000); // 每秒

    // 使用 fetch 或者其他 AJAX 方法将邮箱地址发送到后端蓝图
    fetch('/auth/email/captcha', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({email: email})
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            if (data.code !== 200)
            {
                // 取消定时器并重新启用按钮
                clearInterval(cooldownInterval);
                document.getElementById("sendButton").textContent = "Verify Email";
                document.getElementById("sendButton").disabled = false;
                cooldownTime = 30; // 重置冷却时间
                alert(data.message)
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    // }
}
