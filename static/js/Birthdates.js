let selected = {'year':2000};

let yearProxy = new Proxy(selected, {
    set(target, property, value, receiver) {
      let success = false;
      if (property === 'fullYear') {
          success = Reflect.set(target, 'year', value, receiver);
          if (success) {
            decade(10 * (value % 10));
            year(value % 10);
          }
      }
      if (property === 'decade') {
          success = Reflect.set(target, 'year', value + (target.year % 10), receiver);
          if (success) {
            decade(value);
            year(target.year % 10);
          }
      }
      if (property === 'year') {
          success = Reflect.set(target, 'year', target.year - (target.year % 10) + value, receiver);
          if (success) {
            year(value);
          }
      }
      return success;
    }
});


function decade(value) {
    document.querySelector('.dropdown-toggle').textContent = value;
}



function year(value) {
    document.querySelector('#birthdates').textContent =  yearProxy.year;
    for (let i = 0; i < 10; i++) {
        const yearButton = document.querySelector(`#y-${i}`);
        if (yearButton.classList.contains('active')) {
            yearButton.classList.remove('active');
        }
    }
    for (let i = 0; i < 12; i++) {
      let dt = new Date();
      dt.setFullYear(yearProxy.year, i);
      document.querySelector(`#m-${i}`).textContent = dt.toLocaleString('default', { month: 'long', year: 'numeric' });
    }
    document.querySelector(`#y-${value}`).classList.add('active');
}


async function init() {
  let row = document.querySelector('.dropdown-menu');
  row.onclick = function (event) {
    let button = event.target.closest('button');
    if (!button) return;
    if (!row.contains(button)) return;
    yearProxy.decade = Number(button.textContent);    
  };
  let row2 = document.querySelector('#years');
  row2.onclick = function (event) {
    let button = event.target.closest('button');
    if (!button) return;
    if (!row2.contains(button)) return;
    yearProxy.year = Number(button.textContent);
  };
}


document.addEventListener('DOMContentLoaded', function (event) {
  init();
  yearProxy.fullYear = 1998;
});
