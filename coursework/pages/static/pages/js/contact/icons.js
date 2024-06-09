/* -- ІКОНКИ -- */

/* -- Встаовлення кольору вспливаючого вікна для іконки -- */
document.addEventListener('DOMContentLoaded', function () {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    var colorClass = tooltipTriggerEl.querySelector('i').classList[1].split('-')[1];
    tooltipTriggerEl.setAttribute('data-bs-custom-class', 'tooltip-' + colorClass);
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })
});