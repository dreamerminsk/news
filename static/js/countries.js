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
			   <hr/>
			   <img class="img-fluid rounded shadow-sm" src="${country?.emblem}">
             </div>
             <div class="m-0 p-0 col-6 col-sm-6 col-md-7 col-lg-9">
               <p class="card-text">${country?.wiki?.ru}</p>
               <p class="card-text">${country?.pvi_month?.ru}</p>
               <small class="text-muted">${country?.lasttime?.ru}</small>
               <hr/>
               <p class="card-text">${country?.wiki?.en}</p>
               <p class="card-text">${country?.pvi_month?.en}</p>
               <small class="text-muted">${country?.lasttime?.en}</small>
               <hr/>
               <p class="card-text">${country?.wiki?.uk}</p>
               <p class="card-text">${country?.pvi_month?.uk}</p>
               <small class="text-muted">${country?.lasttime?.uk}</small>
             </div>
           </div>
         </div>
         <div class="card-body text-dark">
           <ul class="nav nav-pills card-header-pills">
  		     <li class="nav-item">
               <a class="nav-link active" href="#">info</a>
             </li>
             <li class="nav-item">
               <a class="nav-link" href="#">racers</a>
             </li>
             <li class="nav-item">
               <a class="nav-link disabled" href="#">races</a>
             </li>
           </ul>
         </div>
       </div>`;
    });
}


document.addEventListener('DOMContentLoaded', function (event) {
  filter();
});
