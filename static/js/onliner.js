async function dbs() {
  let row = document.querySelector('#content');
  let t = ``;
  for(let i = 0; i < 11; i++) {
    let d = new Date();
    d.setUTCDate(d.getUTCDate() + i);
    t += `
    <div class="card text-dark bg-light border-primary mb-3">
      <div class="card-body">
        ${d.toDateString()}
      </div>
    </div>`;
  }
  row.innerHTML = t;
}



async function router() {
  if (window.location.pathname === '/onliner/') {
    await dbs();
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
  history.replaceState({ 'url': '/onliner/' }, '', '/onliner/')
  router();
});
