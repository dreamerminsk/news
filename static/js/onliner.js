let options;

let observer;

let firstDay = new Date();

let lastDay = new Date();


function PrevItems() {
  return `
  <div id="prev-items" class="card text-center fw-bold text-dark bg-light border-dark mx-2 my-4">
      <div class="card-body">
        load
      </div>
  </div>
`;
}


function NextItems() {
  return `
  <div id="next-items" class="card text-center fw-bold text-dark bg-light border-dark mx-2 my-4">
      <div class="card-body">
        load
      </div>
  </div>
    `;
}


function DayView(day) {
  return `
    <div class="card text-dark bg-light border-dark m-2">
	  <div class="card-header">
        ${day.toDateString()}
      </div>
      <ul class="list-group list-group-flush">
        <li class="list-group-item">An item</li>
        <li class="list-group-item">A second item</li>
        <li class="list-group-item">A third item</li>
      </ul>
    </div>`;
}


function addPrevItem() {
  firstDay.setUTCDate(firstDay.getUTCDate() - 1);
  let row = document.querySelector('#days');
  row.insertAdjacentHTML('afterbegin', DayView(firstDay));
}

function addNextItem() {
  lastDay.setUTCDate(lastDay.getUTCDate() + 1);
  let row = document.querySelector('#days');
  row.insertAdjacentHTML('beforeend', DayView(lastDay));
}


async function dbs() {
  let row = document.querySelector('#content');
  row.innerHTML = `${PrevItems()}<div id="days">${DayView(new Date())}</div>${NextItems()}`;
  
  setTimeout(() => {
    for (const x of Array(7).keys()) {
      addPrevItem();
    }
  }, 0);

  setTimeout(() => {
    for (const x of Array(7).keys()) {
      addNextItem();
    }
  }, 0);

  setTimeout(() => {
    let nd = document.getElementById('next-items');
    observer.observe(nd);
    let pd = document.getElementById('prev-items');
    observer.observe(pd);
  }, 0);
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



function intersectionCallback(entries) {
  entries.forEach(function(entry) {
    let adBox = entry.target;
    
    if (entry.isIntersecting) {
      if (adBox.getAttribute('id') === 'prev-items') {
        setTimeout(() => {
          for (const x of Array(4).keys()) {
            addPrevItem();
          }
        }, 0);
      }
      if (adBox.getAttribute('id') === 'next-items') {
        setTimeout(() => {
          for (const x of Array(4).keys()) {
            addNextItem();
          }
        }, 0);
      }
    } else {

    }
  });
}



document.addEventListener('DOMContentLoaded', function (event) {
    options = {
      root: null,
      rootMargin: '0px',
      threshold: 1.0
    }
    observer = new IntersectionObserver(intersectionCallback, options);
    window.addEventListener('popstate', () => router());
    document.addEventListener('click', handleClick);
    history.replaceState({ 'url': '/onliner/' }, '', '/onliner/');
    router();
});
