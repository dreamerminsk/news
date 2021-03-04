async function init(header) {
  let url = `http://ip-api.com/json/${header.dataset.host}`;
  let r = await fetch(url);
  if (r.ok) {
    let json = await r.json();
    header.textContent += ` - ${json.country} - ${json.timezone}`;
    header.setAttribute('data-country', json.country);
    header.className = 'card-header border-primary bg-primary text-white';
  } else {
    header.textContent += ` - ${r.status}`;
    header.className = 'card-header border-danger bg-danger text-white';
  }
}

async function update() {
  let hs = document.querySelectorAll('.card-header');
  let h = hs.find((item) => !item.hasAttribute('data-country'));
  if (h) {
    init(h);
  }
}

document.addEventListener('DOMContentLoaded', function (event) {
  setTimeout(update, Math.floor(Math.random() * 6000) + 2000);
  let hs = document.querySelectorAll('.card-header');
  hs.forEach(function (h, index) {
    setTimeout(init, Math.floor(Math.random() * 3000) + 4000 * index, h);
  });
});
