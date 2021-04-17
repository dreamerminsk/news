let options;

let observer;

let firstDay = new Date();

let lastDay = new Date();


function PrevItems() {
  return `
  <div id="prev-items" class="card text-white bg-secondary border-dark m-3">
      <div class="card-body text-center">
        loading...
      </div>
  </div>
`;
}


function NextItems() {
  return `
  <div id="next-items" class="card text-white bg-secondary border-dark m-3">
      <div class="card-body text-center">
        loading...
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
      <div class="card-body">
        ${day.toDateString()}
      </div>
    </div>`;
}


async function dbs() {
  let row = document.querySelector('#content');
  let t = ``;
  for(let i = 0; i < 7; i++) {
    firstDay.setUTCDate(firstDay.getUTCDate() - 1);
    t = DayView(firstDay) + t;
  }
  for(let i = 0; i < 7; i++) {
    lastDay.setUTCDate(lastDay.getUTCDate() + 1);
    t += DayView(lastDay);
  }
  t = `${PrevItems()}<div id="days">${t}</div>${NextItems()}`;

  row.innerHTML = t;
  let timerId = setTimeout(() => {
    let ld = document.getElementById('next-items');
	observer.observe(ld);
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
		for(let i = 0; i < 4; i++) {
			lastDay.setUTCDate(lastDay.getUTCDate() + 1);
			let row = document.querySelector('#days');
			row.innerHTML += DayView(lastDay);
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
