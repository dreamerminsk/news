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
    <a class='btn btn-outline-info btn-sm' href='#'>${c}</a>
    <a class='btn btn-outline-info btn-sm' href='https://ru.wikipedia.org/wiki/${c}'>
      ru
    </a>
  </div>
  `).join('');
}

function racer_image(r) {
  if (r.image !== null && r.image !== undefined) {
    return `<img class="img-fluid rounded" async src="${r.image.replace('200px', '1000px')}"></img>`;
  } else if (r.images !== null && r.images !== undefined && r.images.length > 0) {
    for (let img of r.images) {
      if (img !== null && img !== undefined) {
        return `<img class="img-fluid rounded" async src="${img}"></img>`;
      }
    }
  }
  else return `
    <img class="img-fluid rounded" async src="https://img.championat.com/i/nopic/person.png"></img>`;
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
        `<div class="card ${racer.wiki.ru.includes('страница отсутствует') ? 'border-danger' : 'border-info'} mb-3">         
         <div class="card-header ${racer.wiki.ru.includes('страница отсутствует') ? 'bg-danger' : 'bg-info'} text-white fw-bold">${racer.wiki.ru}</div>
         <div class="card-body text-dark">
           <div class="row"><div class="col-6">
           <h6 class="card-title">${racer?.name}</h6>
           <p class="card-text">
             <div class="button-toolbar">
               ${country_list(racer.countries ?? [])}
             </div>
           </p>
           <p class="card-text">${new Date(racer?.bday)?.toLocaleDateString()}</p>
           </div><div class="col-6">
             ${racer_image(racer)}
           </div></div>
         </div>
		 <div class="card-body text-dark">
 		   <p class="card-text">${racer?.desc}</p>
                   <p class="card-text"><small class="text-muted">Last updated at ${racer?.last_modified}</small></p>
		 </div>
		 <div class="card-footer text-dark">
                   <div class='btn-group float-right' role='group'>${links(racer)}</div>
		 </div>
       </div>`;
    });
}

function links(racer) {
  let links = `
    <a class="btn btn-outline-info active" href="https://ru.wikipedia.org/wiki/${racer.wiki.ru}">
      <img width="16" height="16" src="https://ru.wikipedia.org/static/favicon/wikipedia.ico">
    </a>`;
  if (racer.champ) {
    links += `
    <a class="btn btn-outline-info" href="https://www.championat.com/biathlon/_biathlonworldcup/tournament/${racer.champ.tournaments[0]}/players/${racer.champ.cc_id}/">
      <img src="https://st.championat.com/i/favicon/favicon-16x16.png">
    </a>`
  }
  return links;
}


async function highlight(td) {
  if (selectedTd) {
    selectedTd.classList.remove('table-primary');
    selectedTd.classList.remove('text-white');
  }
  selectedTd = td;
  selectedTd.classList.add('table-primary');
  selectedTd.classList.add('text-white');
  await filter();
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





function getAge(birthDate) {
  let today = new Date();
  let age = today.getFullYear() - birthDate.getFullYear();
  let m = today.getMonth() - birthDate.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  return age;
}