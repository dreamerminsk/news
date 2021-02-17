async function init() {
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
        <a class="nav-link" data-bs-toggle="pill" id="profile-tab-${index}" href="#profile-${index}" role="tab" aria-controls="profile" aria-selected="false">profile</a>
      </li>
      <li class="nav-item" role="presentation">
        <a class="nav-link data-bs-toggle="pill" id="messages-tab-${index}" href="#messages" role="tab" aria-controls="messages" aria-selected="false">messages</a>
      </li>
    </ul>
  </div>

  <div class="card-body">
    <div class="tab-content">
  <div class="tab-pane  fade show active" id="home-${index}" role="tabpanel" aria-labelledby="home-tab">home-${index}</div>
  <div class="tab-pane  fade show" id="profile-${index}" role="tabpanel" aria-labelledby="profile-tab">profile-${index}</div>
  <div class="tab-pane  fade show" id="messages-${index}" role="tabpanel" aria-labelledby="messages-tab">...</div>
  <div class="tab-pane  fade show" id="settings-${index}" role="tabpanel" aria-labelledby="settings-tab">...</div>
</div>
  </div>
</div>
    `;
  }
  t += ``;
  row.innerHTML += t;
  setInterval(function() {
    var triggerTabList = [].slice.call(document.querySelectorAll('#card-header-pills-0 a'));
    triggerTabList.forEach(function (triggerEl) {
      var tabTrigger = new bootstrap.Tab(triggerEl);

      triggerEl.addEventListener('click', function (event) {
        event.preventDefault();
        tabTrigger.show();
      });
    });
  }, 100);
}


document.addEventListener('DOMContentLoaded', function (event) {
  init();
});
