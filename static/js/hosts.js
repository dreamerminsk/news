async function init(header) {
  url = `http://ip-api.com/json/${header.dataset.host}`;
  let r = await fetch(url);
  if (r.ok) {
    let json = await r.json();
    header.textContent += ` - ${json.country}`;
  }
}

document.addEventListener('DOMContentLoaded', function (event) {
  let hs = document.querySelectorAll('.card-header');
  hs.forEach(function (h, index) {
    setTimeout((h) => init(h), index * 1000);
  });
});
