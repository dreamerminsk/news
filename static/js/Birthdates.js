async function init() {
  let row = document.querySelector('div.querySelector');
  row.onclick = function (event) {
    let button = event.target.closest('button');
    if (!button) return;
    if (!row.contains(button)) return;
    highlight(td);
  };
}


document.addEventListener('DOMContentLoaded', function (event) {
  init();
});
