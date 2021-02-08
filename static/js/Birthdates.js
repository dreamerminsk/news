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
    let d = document.querySelector('.dropdown-toggle').textContent;
    let y = button.textContent;
    document.querySelector('#birthdates').textContent =
      (Number(y) + Number(y)).toString();
    for (let i = 0; i < 12; i++) {
      let d=;
      d.setFullYear(Number(y) + Number(y), i);
      today.toLocaleString('default', { month: 'short' });
    }
  };
}


document.addEventListener('DOMContentLoaded', function (event) {
  init();
});
