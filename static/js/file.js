const fileUpload = document.getElementById('file-upload');
const fileCount = document.getElementById('file-count');

fileUpload.addEventListener('change', function() {
    const files = fileUpload.files;
    if (files.length > 0) {
        fileCount.textContent = `${files.length} فایل انتخاب شده است`;
    } else {
        fileCount.textContent = 'فایلی انتخاب نشده است';
    }
});
