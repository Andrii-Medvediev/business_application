/* -- ЗАВАНТАЖЕННЯ ФОТО  -- */

/* Завантаження та відображення фото */
function previewPhoto() {
  const file = document.getElementById('photo').files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const photoPreview = document.getElementById('photoPreview');
      photoPreview.src = e.target.result;
      photoPreview.style.display = 'block';
      document.querySelector('.photo-upload .icon').style.display = 'none';
    };
    reader.readAsDataURL(file);
  }
}