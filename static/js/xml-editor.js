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
        document.getElementById('messages').innerHTML = url;
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

function errorAlert(e) {
    return
    `<div class="alert alert-danger alert-dismissible fade show" role="alert">
       <button type="button" class="close" data-dismiss="alert" aria-label="Close">
         <span aria-hidden="true">&times;</span>
       </button>
       <strong>${e.name}</strong></hr>${e.message}
     </div>`;
}

function update() {
    let match = document.getElementById('current-name');
    match.innerHTML = `${currentNode.nodeName}`;
}
