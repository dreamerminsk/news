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
    .sort((a, b) => (b?.pvi_month?.ru ?? 0) + (b?.pvi_month?.en ?? 0) - (a?.pvi_month?.ru ?? 0) - (a?.pvi_month?.en ?? 0))
    .forEach(country => {
      node.innerHTML +=
        `<div class="card border-primary mb-3">
         <div class="card-header bg-primary text-white">${country?.wiki?.ru}</div>
         <div class="card-body text-dark">
		   <div class="row">
		     <div class="col-6 col-sm-6 col-md-5 col-lg-3">
			   <img class="img-fluid rounded shadow-sm" src="${country?.flag}">
			 </div>
			 <div class="col-6 col-sm-6 col-md-7 col-lg-9">
			   <p class="card-text">${country?.wiki?.ru}</p>
         <p class="card-text">${country?.pvi_month?.ru}</p>
         <small class="text-muted">${country?.lasttime?.ru}</small>
         <hr/>
         <p class="card-text">${country?.wiki?.en}</p>
			   <p class="card-text">${country?.pvi_month?.en}</p>
         <small class="text-muted">${country?.lasttime?.en}</small>
			 </div>
		   </div>
         </div>
		 <div class="card-body text-dark">
           <p class="card-text"><small class="text-muted">${country?.lasttime?.ru}</small></p>
		 </div>
       </div>`;
    });
}


document.addEventListener('DOMContentLoaded', function (event) {
  filter();
});
