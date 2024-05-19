const text = "In the era of artificial intelligence, deep learning models have revolutionized the way we solve complex problems across various domains. Our gallery showcases a curated collection of state-of-the-art deep learning models along with their applications, offering a glimpse into the vast landscape of AI innovation.";
let index = 0;

function printText() {
  document.getElementById('text').textContent += text[index];
  index++;
  if (index < text.length) {
    setTimeout(printText, 35); // 设置文本显示速度
  }
}

printText();