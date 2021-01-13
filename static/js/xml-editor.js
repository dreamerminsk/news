let xmlDoc;
let currentNode;

async function loadFeed(url) {
  let response = await fetch(url);
  document.getElementById('current-name').innerHtml = url;

  if (response.ok) {
    let text = await response.text();
    let parser = new DOMParser();
    xmlDoc = parser.parseFromString(text, "text/xml");
    currentNode = xmlDoc.documentElement;
    update();
  } else {
    alert("Ошибка HTTP: " + response.status);
  }
}

function update() {
  let match = document.getElementById('current-name');
  match.innerHtml = `${currentNode.nodeName}`;
}



document.addEventListener('DOMContentLoaded', function (event) {
  let source = document.getElementById('source');
  await loadFeed(source.getAttribute('href'));
});
