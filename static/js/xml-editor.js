async function loadFeed(url) {
  let response = await fetch(url);
  let commits = await response.json();
  let parser = new DOMParser();
  let xmlDoc = parser.parseFromString(text,"text/xml");
  let res = await fetch(`/api/feeds/latest`);
  let json = await res.json();
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
