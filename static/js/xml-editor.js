let xmlDoc;
let parentNode;
let currentNode;
let contentNode;
let messagesNode;
let listNodes;


let headers = new Headers({
  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:83.0) Gecko/20100101 Firefox/83.0"
});


document.addEventListener('DOMContentLoaded', function (event) {
  contentNode = document.getElementById('content');
  messagesNode = document.getElementById('messages');
  parentNode = document.getElementById('parent-node');
  parentNode.onclick = parentClick;
  listNodes = document.getElementById('child-nodes');
  listNodes.onclick = nodeClick;
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
    <div class="alert alert-light alert-dismissible fade show m-0 p-2" role="alert" id="${uuidv4()}">
      <h6 class="alert-heading">Loading</h6>
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
      <p class="m-0 p-1"><a href="${getUrl()}" class="alert-link">${getTitle()}</a></p>
    </div>`;
}


function loadedAlert() {
  return `
    <div class="alert alert-info alert-dismissible fade show m-0 p-2" role="alert" id="${uuidv4()}">
      <h6 class="alert-heading">Loaded</h6>
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
      <p><a href="${getUrl()}" class="alert-link">${getTitle()}</a></p>
    </div>`;
}

function errorAlert(e) {
  return `
    <div class="alert alert-danger alert-dismissible fade show m-0 p-2" role="alert">
    <h6 class="alert-heading">${e.name}</h6>
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
      ${e.message}
    </div>`;
}

async function update() {
  let match = document.getElementById('current-node');
  $('#current-node').replaceWith(DetailsCard());

  $('#child-nodes').empty();

  if (currentNode.parentNode) {
    $('#parent-node').empty();
    parentNode.insertAdjacentHTML('beforeend', ParentCard());
  } else {
    $('#parent-node').empty();
  }

  currentNode.childNodes.forEach(function (child, index) {
    if (child.nodeName.startsWith('#')) {
      if (hasValue(child)) {
        listNodes.insertAdjacentHTML('beforeend', ChildCard(child, index));
      }
    } else {
      listNodes.insertAdjacentHTML('beforeend', ChildCard(child, index));
    }
  });
}

function DetailsCard() {
  let attrs = ``;
  if (currentNode.hasAttributes()) {
    attrs += `<ul class="list-group list-group-flush bg-primary">`;
    for (let attr of currentNode.attributes) {
      attrs += `<li class="list-group-item">${attr.name}: ${attr.value}</li>`;
    }
    attrs += `</ul>`;
  }
  return `
    <div id="current-node" class="card text-white fw-bold bg-primary border-dark">
      <div class="card-body">
        <h6 class="card-title">${currentNode.nodeName}</h6>
      </div>
      ${attrs}
    </div>`;
}

function ParentCard() {
  return `
    <div class="card text-white bg-secondary border-dark">
      <div class="card-body">
        <h6 class="card-title">${currentNode.parentNode.nodeName}</h6>
      </div>
    </div>`;
}

function ChildCard(childNode, index) {
  return `
    <div class="card border-dark" data-id="${index}">
      <div class="card-body">
        <h6 class="card-title">${childNode.nodeName}</h6>
        <p>outerHTML: ${(childNode.outerHTML ?? '').length}, innerHTML: ${(childNode.innerHTML ?? '').length}, nodeValue: ${(childNode.nodeValue ?? '').length}</p>
      </div>
      ${NodeValue(childNode)}
    </div>`;
}

function NodeValue(childNode) {
  if (hasValue(childNode)) {
    return `
      <div class="card-body">
        <p class="card-text">${childNode.nodeValue.trim()}</p>
      </div>`;
  }
  return ``;
}

function hasValue(childNode) {
  if (childNode.nodeValue) {
    if (childNode.nodeValue.trim().length > 0) {
      return true;
    }
  }
  return false;
}

async function parentClick(event) {
  let div = event.target.closest('div.card');
  if (!div) return;
  currentNode = currentNode.parentNode;
  await update();
};


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
