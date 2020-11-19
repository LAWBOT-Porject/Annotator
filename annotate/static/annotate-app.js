//Array of list items
const li_tags = document.querySelectorAll('li.file-link');
const p_decision = document.getElementById('file-contents');

const displyTextFile = (evt) => {
    let link = evt.target.getAttribute("data-link");
    evt.target.style.color = 'green';
    fetch(link)
    .then(response => response.text())
    .then(data => {
      p_decision.innerText = data;
    });
}

li_tags.forEach( li => li.addEventListener('click', displyTextFile));
console.log('3');
