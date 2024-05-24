// 获取导航栏中的所有链接
let aList = document.querySelectorAll('.nav-justified li a');
let liList = document.querySelectorAll('.nav-justified li');

// 遍历所有链接
let i = 0
let shouldRedirect = true

aList.forEach(function (link) {
    if (currentPageUrl.includes(link.href)) {
        liList[i].classList.add('active')
        shouldRedirect = false
    }
    i ++
});

if (shouldRedirect) {
    window.location.href = '/admin/analyze'
}


