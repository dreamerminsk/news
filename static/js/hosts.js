async function init(header) {
  let url = `http://ip-api.com/json/${header.dataset.host}`;
  let r = await fetch(url);
  if (r.ok) {
    let json = await r.json();
    header.textContent += ` - ${json.country} - ${json.timezone}`;
    parent = header.parentNode;
    parent.classList.add('border-primary');
    parent.classList.remove('border-dark');
    parent.classList.add('card-primary');
    parent.classList.remove('card-dark');
  } else {
    parent = header.parentNode;
    parent.classList.add('border-danger');
    parent.classList.remove('border-dark');
    parent.classList.add('card-danger');
    parent.classList.remove('card-dark');
  }
}

document.addEventListener('DOMContentLoaded', function (event) {
  let hs = document.querySelectorAll('.card-header');
  hs.forEach(function (h, index) {
    setTimeout(init, Math.floor(Math.random() * 3000) + 2000, h);
  });
});
