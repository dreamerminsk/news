async function loadFeed() {
  let response = await fetch('/api/tasks/feeds');
  let commits = await response.json();
  document.getElementById("task-start").textContent = commits.start.toLocaleString();
  document.getElementById("task-elapsed").textContent = commits.elapsed;
  document.getElementById("task-feeds").textContent = `${commits.feeds}`;
  document.getElementById("task-articles").textContent = `${commits.total - commits.articles}`;
  document.querySelectorAll('div.card').forEach(div => {
    if (div.classList.contains('bg-success')) {
      div.classList.remove('bg-success');
      div.classList.remove('text-white');
    }
  });
  document.querySelectorAll('.table').forEach(div => {
    if (div.classList.contains('text-white')) {
      div.classList.remove('text-white');
    };
  });
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
  loadFeed();
});
