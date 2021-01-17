let xmlDoc;
let currentNode;
const whitespaces = new Set([9, 10, 11, 12, 13, 32, 133, 160, 5760,
  8192, 8193, 8194, 8195, 8196, 8197, 8198, 8199, 8200, 8201,
  8202, 8232, 8233, 8239, 8287, 12288]);

let headers = new Headers({
  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:83.0) Gecko/20100101 Firefox/83.0"
});


document.addEventListener('DOMContentLoaded', function (event) {
  document.getElementById('child-nodes').onclick = nodeClick;
  let content = document.getElementById('content');
  loadFeed(`/api/feeds/${content.dataset.feedId}/source`);
});

async function loadFeed(url) {
  try {
    document.getElementById('messages').innerHTML = loadingAlert(url);
    let response = await fetch(url, {
      method: 'GET',
      headers: headers,
      mode: 'no-cors'
    });

    let text = await response.text();
    let parser = new DOMParser();
    xmlDoc = parser.parseFromString(text, "text/xml");
    currentNode = xmlDoc.documentElement;
    await update();
  } catch (e) {
    document.getElementById('messages').innerHTML = errorAlert(e);
  }
}

function loadingAlert(url) {
  return `
    <div class="alert alert-info alert-dismissible fade show" role="alert">
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
      Loading <a href="${url}" class="alert-link">${url}</a>
    </div>`;
}

function loadedAlert(url) {
  return `
    <div class="alert alert-success alert-dismissible fade show" role="alert">
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
      Loaded <a href="${url}" class="alert-link">${url}</a>
    </div>`;
}

function errorAlert(e) {
  return `
    <div class="alert alert-danger alert-dismissible fade show" role="alert">
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
      <strong>${e.name}</strong> ${e.message}
    </div>`;
}


async function initLetters() {
  const ABC = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ';
  const row = document.getElementById("head-letters");
  row.onclick = function (event) {
    let td = event.target.closest('td');
    if (!td) return;
    if (!row.contains(td)) return;
    highlight(td);
  };
  Array.from(ABC).forEach((e, i) =>
    row.insertAdjacentHTML("beforeend",
      `<td id="letter-${i}" title="${e}">${e}</td>`));
}

async function update() {
  let content = document.getElementById('content');
  document.getElementById('messages').innerHTML = loadedAlert(`/api/feeds/${content.dataset.feedId}/source`);

  let match = document.getElementById('current-name');
  match.innerHTML = `${currentNode.nodeName}`;

  let listNodes = document.getElementById('child-nodes');
  await clearChildNodes();
  currentNode.childNodes.forEach(function (child, index) {
    if (child.nodeName == '#text') {
      listNodes.innerHTML += `
      <div class="card card-body" data-id="${index}">
          <p class="card-text">${child.nodeName}</p>
          <hr/>
          <p>"${child.nodeValue.trim()}"</p>
      </div>`;
    } else {
      listNodes.innerHTML += `
      <div class="card card-body" data-id="${index}">
          <p class="card-text">${child.nodeName}</p>
      </div>`;
    }
  });
}

async function clearChildNodes() {
  document.getElementById('child-nodes').replaceChildren();
}


async function nodeClick(event) {
  let div = event.target.closest('div.card');
  if (!div) return;
  let id = div.dataset.id;
  if (!id) return;
  currentNode = currentNode.childNodes[id];
  await update();
};
