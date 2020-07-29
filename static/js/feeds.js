async function updateFeeds() {
  let response = await fetch('/tasks/feeds');
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
  let res = await fetch(`/feeds/latest`);
  let json = await res.json();
  document.getElementById("feeds").textContent = '';
  json.feeds.forEach(feed => {
    document.getElementById("feeds").textContent += `${feed.title}`;
    let match = document.getElementById(feed['_id']);
    match.classList.add('bg-success');
    match.classList.add('text-white');
    let t = match.querySelector(`.table`);
    t.classList.add('text-white');
    let la = document.getElementById(`la-${id}`);
    la.textContent = feed['last_access'];
    let na = document.getElementById(`na-${id}`);
    na.textContent = feed['next_access'];
    let ttl = document.getElementById(`ttl-${id}`);
    ttl.textContent = feed['ttlf'];
  });
}
let timerId = setTimeout(updateFeeds, 400);
let intervalId = setInterval(updateFeeds, 60000);
