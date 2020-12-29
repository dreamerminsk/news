async function updateRacers() {
  let response = await fetch('/api/ibu/racers');
  let json = await response.json();
  document.getElementById("racers").innerHTML = '';
  json.racers.forEach(racer => {
    try {
      document.getElementById("racers").innerHTML += 
      `<div class="card border-dark mb-3">
         <div class="card-header">${racer.wiki.ru}</div>
         <div class="card-body text-dark">
           <h5 class="card-title">${racer.wiki.ru}</h5>
           <p class="card-text"></p>
           <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>
         </div>
       </div>`;
    } catch (e) {
      document.getElementById("racers").textContent += `${e}`;
    }
  });
}

async function initLetters() {
    const ABC = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ';
    const row = document.getElementById("head-letters");
    try {
    Array.from(ABC).forEach((e, i) => 
        row.insertAdjacentHTML("beforeend",  
        `<td id="letter-${i}" title="${e}">${e}</td>`));
    Array.from(ABC).forEach((e, i) =>
        document.getElementById(`letter-${i}`)
        .addEventListener('click', (ev) => ev.currentTarget.classList.add('table-success')) );
    } catch (ex) {
        row.innerHTML = `<td>${ex}</td>`;
    }
}

let letterId = setTimeout(initLetters, 200);
let timerId = setTimeout(updateRacers, 400);
let intervalId = setInterval(updateRacers, 60000);
