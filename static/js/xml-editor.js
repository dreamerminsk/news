async function loadFeed(url) {
  let response = await fetch(url);

  if (response.ok) {
    let text = await response.text();
    let parser = new DOMParser();
    let xmlDoc = parser.parseFromString(text, "text/xml");
  } else {
    alert("Ошибка HTTP: " + response.status);
  }
  json.feeds.forEach(feed => {
    try {
      let match = document.getElementById(feed['_id']);
      match.classList.add('bg-success');
      match.classList.add('text-white');
      let t = match.querySelector(`.table`);
      t.classList.add('text-white');
      let la = document.getElementById(`la-${feed['_id']}`);
      la.textContent = feed['last_access'];
      let na = document.getElementById(`na-${feed['_id']}`);
      na.textContent = feed['next_access'];
      let ttl = document.getElementById(`ttl-${feed['_id']}`);
      ttl.textContent = feed['ttlf'];
    } catch (e) {
      document.getElementById("feeds").textContent += `${feed['title']}  ${e}`;
    }
  });
}



document.addEventListener('DOMContentLoaded', function (event) {
  let source = document.getElementById('source');
  loadFeed(source.getAttribute('href'));
});
