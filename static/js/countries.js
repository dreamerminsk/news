let countries;

async function loadCountries() {
  let response = await fetch(`/api/ibu/countries/`);
  let json = await response.json();
  seasons = [];
  for (const country of json.countries) {
    countries.push(country);
  }
}

async function filter() {
  const node = document.getElementById("countries");
  node.innerHTML = '';
  await loadCountries();
  countries
    .forEach(country => {
      node.innerHTML +=
        `<div class="card border-primary mb-3">
         <div class="card-header">${country.name}</div>
         <div class="card-body text-dark">
           <h6 class="card-title">${country.title}</h6>
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
