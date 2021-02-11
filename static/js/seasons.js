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
           <div class="card-header bg-primary text-white">${season.wiki.en}</div>
           ${WikiPages(season)}
           <div class="card-footer">
             
           </div>
         </div>`;
    });
}

function WikiPages(season) {
  return Object.keys(season.wiki)
    .sort((a, b) => (season.pvi_month[b] ?? 0) - (season.pvi_month[a] ?? 0))
    .map((lang) => WikiPage(lang, season))
    .join('');
}

function WikiPage(lang, season) {
  return `
  <div class="card-body text-dark">
    <h6 class="card-title">
      <span class="badge bg-primary pe-1">
        <small class="text-white fw-bold">${lang}</small>
      </span>
      ${season.wiki[lang]}</h6>
    <p class="card-text">${season.pvi_month[lang]}
      <small class="text-muted ps-3">${season.lasttime[lang]}</small>
    </p>
  </div>
  `;
}


document.addEventListener('DOMContentLoaded', function (event) {
  filter();
});
