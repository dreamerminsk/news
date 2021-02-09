let selected = {'year':2000};

let yearProxy = new Proxy(selected, {
    set(target, property, value, receiver) {
      let success = false;
      if (property === 'fullYear') {
          success = Reflect.set(target, 'year', value, receiver);
          if (success) {
            localStorage.setItem('fullYear', target.year);
            decade(value - (value % 10));
            year(value % 10);
          }
      }
      if (property === 'decade') {
          success = Reflect.set(target, 'year', value + (target.year % 10), receiver);
          if (success) {
            localStorage.setItem('fullYear', target.year);
            decade(value);
            year(target.year % 10);
          }
      }
      if (property === 'year') {
          success = Reflect.set(target, 'year', target.year - (target.year % 10) + value, receiver);
          if (success) {
            localStorage.setItem('fullYear', target.year);
            year(value);
          }
      }
      return success;
    }
});


function decade(value) {
    document.querySelector('.dropdown-toggle').textContent = value;
}



async function year(value) {
    document.querySelector('#birthdates').textContent =  yearProxy.year;
    for (let i = 0; i < 10; i++) {
        const yearButton = document.querySelector(`#y-${i}`);
        if (yearButton.classList.contains('active')) {
            yearButton.classList.remove('active');
        }
    }
    for (let i = 0; i < 12; i++) {
      let url = `http://172.105.80.145:8000/api/ibu/racers/year/${yearProxy.year}/month/${String(i).padStart(2, '0')}`;
      let page = await fetch(url);
      let json = await page.json(); 
      setTimeout(() => yearMonth(yearProxy.year, i, json.racers));
    }
    document.querySelector(`#y-${value}`).classList.add('active');
}

function yearMonth(year, month, racers) {
    let dt = new Date();
    dt.setFullYear(year, month);
    document.querySelector(`#m-${month}`).textContent = dt.toLocaleString('default', { month: 'long', year: 'numeric' });
    document.querySelector(`#r-${month}`).innerHtml = '';
    for(let racer of racers) {
        document.querySelector(`#r-${month}`).innerHtml += `<p>${racer.name}</p>`;
    }
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
  let fullYear = localStorage.getItem('fullYear');
  if (fullYear) {
      yearProxy.fullYear = fullYear;
  } else {
      yearProxy.fullYear = 1998;
  }
});
