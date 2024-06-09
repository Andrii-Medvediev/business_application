document.addEventListener('DOMContentLoaded', function() {
    const photoInput = document.getElementById('photo');
    const photoPreview = document.getElementById('photoPreview');
    const iconUpload = document.querySelector('.photo-upload .icon');

    if (photoInput) {
        photoInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    photoPreview.src = e.target.result;
                    photoPreview.style.display = 'block';
                    if (iconUpload) {
                        iconUpload.style.display = 'none';
                    }
                }
                reader.readAsDataURL(file);
            }
        });
    }
});


