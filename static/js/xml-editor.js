let xmlDoc;
let currentNode;

let headers = new Headers({
  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:83.0) Gecko/20100101 Firefox/83.0"
});


document.addEventListener('DOMContentLoaded', function (event) {
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
    update();
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

function errorAlert(e) {
  return `
    <div class="alert alert-danger alert-dismissible fade show" role="alert">
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
      <strong>${e.name}</strong></hr>${e.message}
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

function update() {
  let match = document.getElementById('current-name');
  match.innerHTML = `${currentNode.nodeName}`;

  let listNodes = document.getElementById('child-nodes');
  listNodes.innerHTML = '';
  listNodes.onclick = nodeClick;
  currentNode.childNodes.forEach(function (child, index) {
    if (child.nodeName == '#text') {
      listNodes.innerHTML += `
      <div class="card card-body" data-id="${index}">
          <p>${child.nodeName}</p>
          <hr/>
          <p>${child.innerText}</p>
      </div>`;
    } else {
      listNodes.innerHTML += `
      <div class="card card-body" data-id="${index}">
          <p>${child.nodeName}</p>
      </div>`;
    }

  });
}


function nodeClick(event) {
  let div = event.target.closest('div.card');
  if (!div) return;
  let id = div.dataset.id;
  if (!id) return;
  currentNode = currentNode.childNodes[id];
  update();
};
