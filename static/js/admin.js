async function dbs() {
  let row = document.querySelector('#content');
  let url = `/api/admin/dbs`;
  let page = await fetch(url);
  let json = await page.json();
  let t = ``;
  for (let [index, db] of json.dbs.entries()) {
    t += `
    <div class="card text-dark bg-light m-2 text-center">
      <div class="card-body">
        <h5 class="card-title"><a class="link-dark stretched-link" href="/admin/dbs/${db.name}">${db.name}</a></h5>
        <p class="card-text">${db.sizeOnDisk}</p>
      </div>
    </div>
    `;
  }
  row.innerHTML = t;
}



async function db(name) {
  let row = document.querySelector('#content');
  let url = `/api/admin/dbs/${name}`;
  let page = await fetch(url);
  let json = await page.json();
  let dbstats = json.dbstats;
  let lis = Object.getOwnPropertyNames(dbstats).map((key) => {
    return `<li class="list-group-item">${key}: ${dbstats[key]}</li>`;
  }).join('');
  let t = `
    <div class="card text-dark bg-light m-2 text-center">
      <div class="card-body">
        <h5 class="card-title">${name}</h5>
      </div>
    </div>
    `;
  t += `
  <div class="accordion m-2" id="accordionExample">
    <div class="accordion-item">
      <h2 class="accordion-header" id="headingOne">
        <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
          dbstats
        </button>
      </h2>
      <div id="collapseOne" class="accordion-collapse collapse" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
        <div class="accordion-body">
          <ul class="list-group list-group-flush">
            ${lis}
          </ul>
        </div>
      </div>
    </div>
  </div>
  `;
  let curl = `/api/admin/dbs/${name}/colls`;
  let cpage = await fetch(curl);
  let cjson = await cpage.json();
  let colls = cjson.colls;
  let lics = colls.map((coll) => {
    return `<li class="list-group-item"><a href="/api/admin/dbs/${name}/colls/${coll}">${coll}</a></li>`;
  }).join('');
  t += `
  <div class="accordion m-2" id="accordionColls">
    <div class="accordion-item">
      <h2 class="accordion-header" id="headingTwo">
        <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
          colls
        </button>
      </h2>
      <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionColl">
        <div class="accordion-body">
          <ul class="list-group list-group-flush">
            ${lics}
          </ul>
        </div>
      </div>
    </div>
  </div>
  `;
  row.innerHTML = t;
}



async function router() {
  if (window.location.pathname === '/admin/dbs') {
    await dbs();
  }
  if (window.location.pathname.startsWith('/admin/dbs/')) {
    let name = window.location.pathname.replace('/admin/dbs/', '')
    await db(name);
  }
}



function findLink(el) {
  if (el.tagName == 'A' && el.href) {
    return el.href;
  } else if (el.parentElement) {
    return findLink(el.parentElement);
  } else {
    return null;
  }
};



function handleClick(e) {
  const link = findLink(e.target);
  if (link == null) {
    return;
  }
  e.preventDefault();
  history.pushState({ 'url': link }, '', link);
  router();
};



document.addEventListener('DOMContentLoaded', function (event) {
  window.addEventListener('popstate', () => router());
  document.addEventListener('click', handleClick);
  history.replaceState({ 'url': '/admin/dbs' }, '', '/admin/dbs')
  router();
});
