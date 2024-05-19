// 获取当前页面的 URL
let currentPageUrl = window.location.href;

// 获取导航栏中的所有链接
let navLinks = document.querySelectorAll('.navbar .navbar-nav li a');

// 遍历所有链接
navLinks.forEach(function (link) {
    if (link.href === currentPageUrl) {
        link.classList.add('active');
    }
});