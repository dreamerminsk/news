async function init2() {
  let row = document.querySelector('#content');
  let url = `/api/admin/dbs`;
  let page = await fetch(url);
  let json = await page.json();
  let t = ``;
  for (let [index, db] of json.dbs.entries()) {
    t += `
    <div class="card text-center">
      <div class="card-header">
        <ul class="nav nav-pills card-header-pills" id="card-header-pills-${index}" role="tablist">
          <li class="nav-item" role="presentation">
            <a class="nav-link active" data-bs-toggle="pill" id="home-tab-${index}" href="#home-${index}" role="tab" aria-controls="home" aria-selected="true">${db.name}</a>
          </li>
          <li class="nav-item" role="presentation">
            <a class="nav-link" data-bs-toggle="pill" id="collections-tab-${index}" href="#collections-${index}" role="tab" aria-controls="profile" aria-selected="false">collections</a>
          </li>
          <li class="nav-item" role="presentation">
            <a class="nav-link data-bs-toggle="pill" id="messages-tab-${index}" href="#messages-${index}" role="tab" aria-controls="messages" aria-selected="false">messages</a>
          </li>
        </ul>
      </div>

      <div class="card-body">
        <div class="tab-content">
          <div class="tab-pane  fade show active" id="home-${index}" role="tabpanel" aria-labelledby="home-tab">
            home-${index}
          </div>
          <div class="tab-pane  fade show" id="collections-${index}" role="tabpanel" aria-labelledby="profile-tab">collections-${index}</div>
          <div class="tab-pane  fade show" id="messages-${index}" role="tabpanel" aria-labelledby="messages-tab">messages-${index}</div>
          <div class="tab-pane  fade show" id="settings-${index}" role="tabpanel" aria-labelledby="settings-tab">...</div>
        </div>
      </div>
    </div>
    `;
    setInterval(function () {
      var triggerTabList = [].slice.call(document.querySelectorAll(`#card-header-pills-${index} a`));
      triggerTabList.forEach(function (triggerEl) {
        var tabTrigger = new bootstrap.Tab(triggerEl);

        triggerEl.addEventListener('click', function (event) {
          event.preventDefault();
          tabTrigger.show();
        });
      });
    }, 100);
  }
  row.innerHTML += t;
}



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
  <div class="accordion" id="accordionExample">
    <div class="accordion-item">
      <h2 class="accordion-header" id="headingOne">
        <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
          dbstats
        </button>
      </h2>
      <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
        <div class="accordion-body">
          <div class="card text-dark bg-light m-2 text-center">
            <ul class="list-group list-group-flush">
              ${lis}
            </ul>
          </div>
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
