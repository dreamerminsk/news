let selected = {'year':2000};

let yearProxy = new Proxy(selected, {
    set(target, property, value, receiver) {
      let success = false;
      if (property === 'decade') {
          success = Reflect.set(target, 'year', value + (target.year % 10), receiver);
          if (success) {
            decade(value);
          }
      }
      if (property === 'year') {
          success = Reflect.set(target, 'year', target.year - (target.year % 10) + value, receiver);
          if (success) {
            handler(property, value);
          }
      }
      return success;
    }
});


function decade(value) {
    document.querySelector('.dropdown-toggle').textContent = value;
}


async function init() {
  let row = document.querySelector('.dropdown-menu');
  row.onclick = function (event) {
    let button = event.target.closest('button');
    if (!button) return;
    if (!row.contains(button)) return;
    selected.decade = Number(button.textContent);    
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
      let dt=new Date();
      dt.setFullYear(Number(d) + Number(y), i);
      document.querySelector(`#m-${i}`).textContent = dt.toLocaleString('default', { month: 'long', year: 'numeric' });
    }
  };
}


document.addEventListener('DOMContentLoaded', function (event) {
  init();
});
