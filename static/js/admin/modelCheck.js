$(
    function () {
        var chart = echarts.init(document.getElementById('bar'), 'pink', {renderer: 'canvas'});
        $.ajax({
            type: "GET",
            url: "/admin/modelPanels/aptChart",
            dataType: 'json',
            success: function (result) {
                chart.setOption(result);
            }
        });
    }
)
