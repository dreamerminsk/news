let xmlDoc;
let currentNode;

let headers = new Headers({
    "User-Agent"   : "Mozilla/5.0 (Windows NT 6.1; rv:83.0) Gecko/20100101 Firefox/83.0"
});

async function loadFeed(url) {
try {
  document.getElementById('messages').innerHTML = url;
  let response = await fetch(url, {
    method  : 'GET', 
    headers : headers,
    mode:'no-cors'});
  alert(`${response}`);

  if (response.ok) {
    let text = await response.text();
    let parser = new DOMParser();
    xmlDoc = parser.parseFromString(text, "text/xml");
    currentNode = xmlDoc.documentElement;
    update();
  } else {
    alert("Ошибка HTTP: " + await response.text());
  }
} catch(e) {
document.getElementById('messages').innerHTML = 
    `<div class="alert alert-danger alert-dismissible fade show" role="alert">
       <button type="button" class="close" data-dismiss="alert" aria-label="Close">
         <span aria-hidden="true">&times;</span>
       </button>
       ${e}
     </div>`;
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
