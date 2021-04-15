var options = {
    root: null,
    rootMargin: '0px',
    threshold: 1.0
}
var callback = function(entries, observer) {
    /* Content excerpted, show below */
};
var observer = new IntersectionObserver(callback, options);



async function dbs() {
  let row = document.querySelector('#content');
  let t = ``;
  for(let i = 0; i < 11; i++) {
    let d = new Date();
    d.setUTCDate(d.getUTCDate() + i);
    t += `
    <div class="card text-dark bg-light border-dark m-2">
      <div class="card-body">
        <button type="button" class="btn btn-secondary">${d.toDateString()}</button>
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
