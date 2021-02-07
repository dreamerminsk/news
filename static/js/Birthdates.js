async function init() {
  let row = document.querySelector('.dropdown-menu');
  row.onclick = function (event) {
    let button = event.target.closest('button');
    if (!button) return;
    if (!row.contains(button)) return;
    document.querySelector('.dropdown-toggle').innerText = button.text()
  };
}


document.addEventListener('DOMContentLoaded', function (event) {
  init();
});
