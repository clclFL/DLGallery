$(document).ready(function() {
    $('.panel').on('click', function() {
        var targetUrl = $(this).data('target-url'); // 使用jQuery的data方法获取属性值
        window.location.href = targetUrl;
    });
});