let racers;
let selectedTd;

async function loadRacers() {
  let response = await fetch(`/api/ibu/racers/names/${selectedTd.title}`);
  let json = await response.json();
  racers = [];
  for (const racer of json.racers) {
    racers.push(racer);
  }
}

function country_list(countries) {
  return countries.map((c) => `
  <div class='btn-group mr-1'>
  <a class='btn btn-outline-dark btn-sm' href='#'>${c}</a>
  <a class='btn btn-outline-dark btn-sm' href='https://ru.wikipedia.org/wiki/${c}'>
    ru
  </a>
  </div>
  `).join('');
}

async function filter() {
  if (!selectedTd) return;
  const node = document.getElementById("racers");
  node.innerHTML = '';
  await loadRacers();
  racers
    .sort((a, b) => a.wiki.ru.localeCompare(b.wiki.ru))
    .forEach(racer => {
      node.innerHTML +=
        `<div class="card border-dark mb-3">
         <img class="card-img-top" src="${racer.image}">
         <div class="card-header">${racer.wiki.ru}</div>
         <div class="card-body text-dark">
           <h6 class="card-title">${racer.name}</h6>
           <p class="card-text">
             <div class="button-toolbar">
               ${country_list(racer.countries)}
             </div>
           </p>
           <p class="card-text">${new Date(racer.bday)?.toLocaleDateString()}</p>
           <p class="card-text"><small class="text-muted">Last updated at ${racer.last_modified}</small></p>
         </div>
       </div>`;
    });
}


async function highlight(td) {
  if (selectedTd) {
    selectedTd.classList.remove('table-success');
  }
  selectedTd = td;
  await filter();
  selectedTd.classList.add('table-success');
}

async function initLetters() {
  const ABC = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ';
  const row = document.getElementById("head-letters");
  row.onclick = function (event) {
    let td = event.target.closest('td');
    if (!td) return;
    if (!row.contains(td)) return;
    highlight(td);
  };
  Array.from(ABC).forEach((e, i) =>
    row.insertAdjacentHTML("beforeend",
      `<td id="letter-${i}" title="${e}">${e}</td>`));
}


document.addEventListener('DOMContentLoaded', function (event) {
  initLetters();
});
