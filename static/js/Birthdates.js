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
      (Number(d) + Number(y)).toString();
    for (let i = 0; i < 12; i++) {
      let d=new Date();
      d.setFullYear(Number(y) + Number(y), i);
      document.querySelector(`#m-${i}`).textContent = d.toLocaleString('default', { month: 'long', year: 'numeric' });
    }
  };
}


document.addEventListener('DOMContentLoaded', function (event) {
  init();
});
