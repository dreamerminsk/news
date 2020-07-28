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
  let feeds = await res.json();
  feeds.ids.forEach(feed => {
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

let timerId = setInterval(updateFeeds, 60000);

function toString(sec) {
  let measuredTime = new Date(null);
  measuredTime.setSeconds(sec);
  return measuredTime.toISOString().substr(11, 8);
}
