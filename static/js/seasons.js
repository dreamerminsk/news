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
        `<div class="card border-primary mb-3">
           <div class="card-header bg-primary text-white">${season.title}</div>
           <div class="card-body text-dark">
             <h6 class="card-title">${season.wiki.en}</h6>
             <p class="card-text">${season.pvi_month.en}</p>
           </div>
           <div class="card-body text-dark">
             <h6 class="card-title">${season.wiki.de}</h6>
             <p class="card-text">${season.pvi_month.de}</p>
           </div>
           <div class="card-body text-dark">
             <h6 class="card-title">${season.wiki.ru}</h6>
             <p class="card-text">${season.pvi_month.ru}</p>
           </div>
           <div class="card-body text-dark">
             <p class="card-text"><small class="text-muted">${season.lasttime}</small></p>
           </div>
         </div>`;
    });
}

function WikiPages(season) {
  
}

function WikiPage(lang, season) {
  return `
  <div class="card-body text-dark">
    <h6 class="card-title">${season.wiki[lang]}</h6>
    <p class="card-text">${season.pvi_month[lang]}</p>
  </div>
  `;
}


document.addEventListener('DOMContentLoaded', function (event) {
  filter();
});
