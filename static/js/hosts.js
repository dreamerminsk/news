async function init(header) {
  let url = `http://ip-api.com/json/${header.dataset.host}`;
  let r = await fetch(url);
  if (r.ok) {
    let json = await r.json();
    header.textContent += ` - ${json.country} - ${json.timezone}`;
    header.setAttribute('data-country', json.country);
    header.className = 'card-header border-success bg-success text-white';
  } else {
    header.textContent += ` - ${r.status}`;
    header.className = 'card-header border-danger bg-danger text-white';
  }
}

async function update() {
  let hs = document.querySelectorAll('.card-header');
  alert(hs);
  let h = hs.find(function(item) {
    return !item.hasAttribute('data-country')
  });
  alert(h);
  if (h) {
    init(h);
  }
}

document.addEventListener('DOMContentLoaded', function (event) {
  setTimeout(update, Math.floor(Math.random() * 6000) + 2000);
});
