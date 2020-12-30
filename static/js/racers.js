let racers = [];
let selectedTd;

async function updateRacers() {
  let response = await fetch('/api/ibu/racers');
  let json = await response.json();
  if (json.racers) {
    racers = [];
    racers.append(json.racers);
  }
}

function filter() {
  if (!selectedTd) return;
  const node = document.getElementById("racers");
  node.innerHTML = '';
  racers.filter(racer => racer.startsWith(selectedTd.title)).forEach(racer => {
      node.innerHTML += 
      `<div class="card border-dark mb-3">
         <div class="card-header">${racer.wiki.ru}</div>
         <div class="card-body text-dark">
           <h5 class="card-title">${racer.wiki.ru}</h5>
           <p class="card-text"></p>
           <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>
         </div>
       </div>`;
  });
}


function highlight(td) {
  if (selectedTd) {
    selectedTd.classList.remove('table-success');
  }
  selectedTd = td;
  filter();
  selectedTd.classList.add('table-success');
}

async function initLetters() {
    const ABC = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ';
    const row = document.getElementById("head-letters");
    row.onclick = function(event) {
        let td = event.target.closest('td');
        if (!td) return;
        if (!row.contains(td)) return;
        highlight(td);
    };
    Array.from(ABC).forEach((e, i) => 
        row.insertAdjacentHTML("beforeend",  
        `<td id="letter-${i}" title="${e}">${e}</td>`));
}


document.addEventListener('DOMContentLoaded', function(event) {
    initLetters();
    updateRacers();
});

let intervalId = setInterval(updateRacers, 60000);
