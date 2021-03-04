async function init(header) {
  let url = `http://ip-api.com/json/${header.dataset.host}`;
  let r = await fetch(url);
  if (r.ok) {
    let json = await r.json();
    header.textContent += ` - ${json.country} - ${json.timezone}`;
    header.classList.add('border-primary');
    header.classList.add('bg-primary');
    header.classList.add('text-white');
  } else {
    header.textContent += ` - ${r.status}`;
    header.classList.add('border-danger');
    header.classList.add('bg-danger');
    header.classList.add('text-white');
  }
}

async function update() {
  let hs = document.querySelectorAll('.card-header');
}

document.addEventListener('DOMContentLoaded', function (event) {
  setTimeout(update, Math.floor(Math.random() * 6000) + 2000);
  let hs = document.querySelectorAll('.card-header');
  hs.forEach(function (h, index) {
    setTimeout(init, Math.floor(Math.random() * 3000) + 4000 * index, h);
  });
});
