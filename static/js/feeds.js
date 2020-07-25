  async function updateFeeds() {
    let response = await fetch('/feeds/update');
    let commits = await response.json();
    document.querySelectorAll('div.card').forEach(div => {
      if (div.classList.contains('bg-success')) {
        div.classList.remove('bg-success');
        div.classList.remove('text-white');
      }
    });
    document.querySelectorAll('.table').forEach(div => {
      if (div.classList.contains('table-success')) {
        div.classList.remove('table-success');
        div.classList.remove('text-white');
      }
    });
    commits.ids.forEach(id => {
      let match = document.getElementById(id);
      match.classList.add('bg-success');
      match.classList.add('text-white');
      let t = document.querySelector(`#${id} .table`);
      t.classList.add('table-success');
      t.classList.add('text-white');
    });
    commits.ids.forEach(async id => {
      let res = await fetch(`/feeds/${id}`);
      let feed = await res.json();
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
