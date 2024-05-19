const text = "Welcome to the world of deeplearning!";
let index = 0;

function printText() {
    document.getElementById('text').textContent += text[index];
    index++;
    if (index < text.length) {
        setTimeout(printText, 35); // 设置文本显示速度
    }
}

printText();

setTimeout(function () {
    window.location.href = 'login'; // 设置要跳转的页面URL
}, 5000); // 3000 毫秒即三秒
