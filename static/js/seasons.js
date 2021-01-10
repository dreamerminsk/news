let seasons;

async function loadSeasons() {
  let response = await fetch(`/api/ibu/seasons/`);
  let json = await response.json();
  seasons = [];
  for (const season of json.seasons) {
    seasons.push(season);
  }
}

async function filter() {
  const node = document.getElementById("seasons");
  node.innerHTML = '';
  await loadSeasons();
  seasons
    .forEach(season => {
      node.innerHTML +=
        `<div class="card border-dark mb-3">
         <div class="card-header">${season.title}</div>
         <div class="card-body text-dark">
           <h6 class="card-title">${season.title}</h6>
         </div>
		 <div class="card-body text-dark">
           <p class="card-text"><small class="text-muted">Last updated at ...</small></p>
		 </div>
       </div>`;
    });
}


document.addEventListener('DOMContentLoaded', function (event) {
  filter();
});
