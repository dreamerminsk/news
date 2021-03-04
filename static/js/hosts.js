function init(header) {

}

document.addEventListener('DOMContentLoaded', function (event) {
  let hs = document.querySelectorAll('.card-header');
  hs.forEach(function (h, index) {
    setTimeout((h) => init(h), index * 1000);
  });
});
