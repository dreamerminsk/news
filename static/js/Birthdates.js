async function init() {
  let row = document.querySelector('.dropdown-menu');
  row.onclick = function (event) {
    let button = event.target.closest('button');
    if (!button) return;
    if (!row.contains(button)) return;
    document.querySelector('.dropdown-toggle').textContent = button.textContent;
  };
  let row2 = document.querySelector('#years');
  row2.onclick = function (event) {
    let button = event.target.closest('button');
    if (!button) return;
    if (!row2.contains(button)) return;
    document.querySelector('#birthdates').textContent =
      (Number(document.querySelector('.dropdown-toggle').textContent) + Number(button.textContent)).toString();
  };
}


document.addEventListener('DOMContentLoaded', function (event) {
  init();
});
