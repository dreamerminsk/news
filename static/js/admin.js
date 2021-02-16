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
  let t = ``;
  for (let db of json.dbs) {
    t += `
    <div class="card text-center">
  <div class="card-header">
    <ul class="nav nav-pills card-header-pills">
      <li class="nav-item">
        <a class="nav-link active" href="#">${db.name}</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Link</a>
      </li>
      <li class="nav-item">
        <a class="nav-link href="#">Disabled</a>
      </li>
    </ul>
  </div>
  <div class="card-body">
    <h5 class="card-title">${db.sizeOnDisk}</h5>
    <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>
    `;
  }
  t += ``;
  row.innerHTML += t;
}


document.addEventListener('DOMContentLoaded', function (event) {
  init();
});
