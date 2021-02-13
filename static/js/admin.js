let selected = { 'year': 2000 };

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




async function init() {
  let row = document.querySelector('#content');
  let url = `/api/admin/dbs`;
  let page = await fetch(url);
  let json = await page.json();
  for (let db of json.dbs) {
    row.innerHTML += `<tr><th scope="row">${db.name}</th><td></td></tr>`;
  }
}


document.addEventListener('DOMContentLoaded', function (event) {
  init();
});
