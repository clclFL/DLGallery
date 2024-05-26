document.getElementById('image-upload').addEventListener('change', function (e) {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById('image-preview').src = e.target.result;
        document.getElementById('submit-button').disabled = false;
    };
    reader.readAsDataURL(file);
});
document.getElementById('submit-button').addEventListener('click', function () {
    const fileInput = document.getElementById('image-upload');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    fetch('/gallery/models/idcardscanning', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('图片上传失败');
            }
            // 这里可以根据后端返回的数据做进一步处理，比如显示成功消息
            return response.json()
        }).then(data => {
            // alert(data.data)
        document.getElementById('image-result').src = '/static/' + data.data
    })
        .catch(error => {
            console.error('Error:', error);
        });
});

document.getElementById('image-upload-2').addEventListener('change', function (e) {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById('image-preview-2').src = e.target.result;
        document.getElementById('submit-button-2').disabled = false;
    };
    reader.readAsDataURL(file);
});
document.getElementById('submit-button-2').addEventListener('click', function () {
    const fileInput = document.getElementById('image-upload-2');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    fetch('/gallery/models/analyzeText', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('图片上传失败');
            }
            // 这里可以根据后端返回的数据做进一步处理，比如显示成功消息
            return response.json()
        }).then(data => {
            // alert(data.data)
        document.getElementById('image-result-2').src = '/static/' + data.data
    })
        .catch(error => {
            console.error('Error:', error);
        });

});

document.getElementById('image-upload-3').addEventListener('change', function (e) {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById('image-preview-3').src = e.target.result;
        document.getElementById('submit-button-3').disabled = false;
    };
    reader.readAsDataURL(file);
});
document.getElementById('submit-button-3').addEventListener('click', function () {
    const fileInput = document.getElementById('image-upload-3');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    fetch('/gallery/models/getText', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('图片上传失败');
            }
            // 这里可以根据后端返回的数据做进一步处理，比如显示成功消息
            return response.json()
        }).then(data => {
            // alert(data.data)
        document.getElementById('my-fault').innerHTML = JSON.stringify(data.data)
    })
        .catch(error => {
            console.error('Error:', error);
        });

});

