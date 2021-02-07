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
			   <img class="img-fluid rounded shadow-sm" src="${country?.emblem ?? 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Herb_%C5%81ab%C4%99d%C5%BA_1.svg/1024px-Herb_%C5%81ab%C4%99d%C5%BA_1.svg.png'}">
             </div>
             <div class="m-0 p-0 col-6 col-sm-6 col-md-7 col-lg-9">
               <p class="m-0 p-0 card-text">${country?.wiki?.ru}</p>
               <p class="m-0 p-0 card-text">${country?.pvi_month?.ru}</p>
               <small class="m-0 p-0 text-muted">${country?.lasttime?.ru}</small>
               <hr/>
               <p class="m-0 p-0 card-text">${country?.wiki?.en}</p>
               <p class="m-0 p-0 card-text">${country?.pvi_month?.en}</p>
               <small class="m-0 p-0 text-muted">${country?.lasttime?.en}</small>
               <hr/>
               <p class="m-0 p-0 card-text">${country?.wiki?.de}</p>
               <p class="m-0 p-0 card-text">${country?.pvi_month?.de}</p>
               <small class="m-0 p-0 text-muted">${country?.lasttime?.de}</small>
               <hr/>
               <p class="m-0 p-0 card-text">${country?.wiki?.fr}</p>
               <p class="m-0 p-0 card-text">${country?.pvi_month?.fr}</p>
               <small class="m-0 p-0 text-muted">${country?.lasttime?.fr}</small>
             </div>
           </div>
         </div>
         <div class="card-body text-dark">
           <ul class="nav nav-pills card-header-pills" id="pills-tab" role="tablist">
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
