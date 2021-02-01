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
    return `<img class="img-fluid rounded border-info border-3" async src="${r.image.replace('200px', '1000px')}"></img>`;
  } else if (r.images !== null && r.images !== undefined && r.images.length > 0) {
    for (let img of r.images) {
      if (img !== null && img !== undefined) {
        return `<img class="img-fluid rounded border-info border-3" async src="${img}"></img>`;
      }
    }    
  }
  else return '';
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
        `<div class="card border-info mb-3">         
         <div class="card-header bg-info text-white fw-bold">${racer.wiki.ru}</div>
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
                   ${links(racer)}
		 </div>
       </div>`;
    });
}
      
function links(racer) {
      var links = `<a href=""></a>`;
      return links;
}


async function highlight(td) {
  if (selectedTd) {
    selectedTd.classList.remove('table-info');
    selectedTd.classList.remove('text-white');
  }
  selectedTd = td;
  selectedTd.classList.add('table-info');
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
