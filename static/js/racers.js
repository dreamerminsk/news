async function updateRacers() {
  let response = await fetch('/api/ibu/racers');
  let json = await response.json();
  document.getElementById("racers").innerHTML = '';
  json.racers.forEach(racer => {
    try {
      document.getElementById("racers").innerHTML += `<div class='container'>${racer.wiki.ru}</div>`;
    } catch (e) {
      document.getElementById("racers").textContent += `${e}`;
    }
  });
}


let timerId = setTimeout(updateRacers, 400);
let intervalId = setInterval(updateRacers, 60000);
