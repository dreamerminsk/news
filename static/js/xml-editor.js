let xmlDoc;
let currentNode;
let contentNode;
let messagesNode;
let listNodes;


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
    messagesNode.insertAdjacentHTML("beforeend", loadingAlert());
    let response = await fetch(getUrl(), {
      method: 'GET',
      headers: headers
    });

    let text = await response.text();
    let parser = new DOMParser();
    xmlDoc = parser.parseFromString(text, "text/xml");
    currentNode = xmlDoc.documentElement;
    messagesNode.insertAdjacentHTML("beforeend", loadedAlert());
    await update();
  } catch (e) {
    messagesNode.insertAdjacentHTML("beforeend", errorAlert(e));
  }
}

function loadingAlert() {
  return `
    <div class="alert alert-secondary alert-dismissible fade show m-0 p-1" role="alert" id="${uuidv4()}">
      <h6 class="alert-heading">Loading</h6>
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
      <p><a href="${getUrl()}" class="alert-link">${getTitle()}</a></p>
    </div>`;
}


function loadedAlert() {
  return `
    <div class="alert alert-info alert-dismissible fade show m-0 p-1" role="alert" id="${uuidv4()}">
      <h6 class="alert-heading">Loaded</h6>
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
      <p><a href="${getUrl()}" class="alert-link">${getTitle()}</a></p>
    </div>`;
}

function errorAlert(e) {
  return `
    <div class="alert alert-danger alert-dismissible fade show m-0 p-1" role="alert">
    <h6 class="alert-heading">${e.name}</h6>
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
      ${e.message}
    </div>`;
}

async function update() {
  let match = document.getElementById('current-name');
  match.innerHTML = `${currentNode.nodeName}`;

  await clearChildNodes();
  currentNode.childNodes.forEach(function (child, index) {
    if (child.nodeValue) {
      if (child.nodeValue.trim().length > 0) {
        listNodes.innerHTML += `
      <div class="card border-dark" data-id="${index}">
        <div class="card-body">
          <h6 class="card-title">${child.nodeName}</h6>
        </div>
        <div class="card-body">
          <p class="card-text">"${child.nodeValue.trim()}"</p>
        </div>
      </div>`;
      }
    } else {
      listNodes.innerHTML += `
      <div class="card border-dark" data-id="${index}">
        <div class="card-body">
          <h6 class="card-title">${child.nodeName}</h6>
        </div>
      </div>`;
    }
  });
}

async function clearChildNodes() {
  $('#child-nodes').empty();
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
