let xmlDoc;
let currentNode;
let contentNode;
let messagesNode;
let listNodes;
const whitespaces = new Set([9, 10, 11, 12, 13, 32, 133, 160, 5760,
  8192, 8193, 8194, 8195, 8196, 8197, 8198, 8199, 8200, 8201,
  8202, 8232, 8233, 8239, 8287, 12288]);

let headers = new Headers({
  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:83.0) Gecko/20100101 Firefox/83.0"
});


document.addEventListener('DOMContentLoaded', function (event) {
  document.getElementById('child-nodes').onclick = nodeClick;
  contentNode = document.getElementById('content');
  messagesNode = document.getElementById('messages');
  listNodes = document.getElementById('child-nodes');
  loadFeed();
});

async function loadFeed() {
  try {
    messagesNode.innerHTML = loadingAlert();
    let response = await fetch(getUrl(), {
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
    messagesNode.innerHTML = errorAlert(e);
  }
}

function loadingAlert() {
  return `
    <div class="alert alert-info alert-dismissible fade show" role="alert">
      <h6 class="alert-heading">Loading</h6>
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
      <p><a href="${getUrl()}" class="alert-link">${getTitle()}</a></p>
    </div>`;
}


function loadedAlert() {
  return `
    <div class="alert alert-info alert-dismissible fade show" role="alert">
      <h6 class="alert-heading">Loaded</h6>
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
      <p><a href="${getUrl()}" class="alert-link">${getTitle()}</a></p>
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
  messagesNode.innerHTML = loadedAlert(`/api/feeds/${content.dataset.feedId}/source`);

  let match = document.getElementById('current-name');
  match.innerHTML = `${currentNode.nodeName}`;

  await clearChildNodes(listNodes);
  currentNode.childNodes.forEach(function (child, index) {
    if (child.nodeName == '#text') {
      if (child.nodeValue.trim().length > 0) {
        listNodes.innerHTML += `
      <div class="card card-body" data-id="${index}">
          <p class="card-text">${child.nodeName}</p>
          <p class="card-text">"${child.nodeValue.trim()}"</p>
      </div>`;
      }
    } else {
      listNodes.innerHTML += `
      <div class="card card-body" data-id="${index}">
          <p class="card-text">${child.nodeName}</p>
      </div>`;
    }
  });
}

async function clearChildNodes(root) {
  root.replaceChildren();
}


async function nodeClick(event) {
  let div = event.target.closest('div.card');
  if (!div) return;
  let id = div.dataset.id;
  if (!id) return;
  currentNode = currentNode.childNodes[id];
  await update();
};

function getUrl() {
  return `/api/feeds/${contentNode.dataset.feedId}/source`;
}

function getTitle() {
  return `${contentNode.dataset.feedTitle}`;
}
