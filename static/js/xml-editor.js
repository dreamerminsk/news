let xmlDoc;
let currentNode;

async function loadFeed(url) {
try {
  document.getElementById('messages').innerHTML = url;
  let response = await fetch(url, {mode:'cors'});
  alert(`${response}`);

  if (response.ok) {
    let text = await response.text();
    let parser = new DOMParser();
    xmlDoc = parser.parseFromString(text, "text/xml");
    currentNode = xmlDoc.documentElement;
    update();
  } else {
    alert("Ошибка HTTP: " + response.status);
  }
} catch(e) {
document.getElementById('messages').innerHTML = `${e}`;
}
}

function update() {
  let match = document.getElementById('current-name');
  match.innerHTML = `${currentNode.nodeName}`;
}



document.addEventListener('DOMContentLoaded', function (event) {
  let source = document.getElementById('source');
  loadFeed(source.getAttribute('href'));
});
