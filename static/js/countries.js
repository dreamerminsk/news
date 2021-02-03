let countries;

async function loadCountries() {
  let response = await fetch(`/api/ibu/countries/`);
  let json = await response.json();
  countries = [];
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
         <div class="card-header">${country.wiki.ru}</div>
         <div class="card-body text-dark">
		   <div class="row">
		     <div class="col-xs-6 col-sm-6 col-md-5 col-lg-3">
			   <img class="img-fluid" src="${country.flag}">
			 </div>
			 <div class="col-xs-6 col-sm-6 col-md-7 col-lg-9">
			   <h6 class="card-title">${country.wiki.ru}</h6>
			 </div>
		   </div>
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
