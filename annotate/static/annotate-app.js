/* Author : Sid Ali MAHMOUDI @ 20/11/2020 */

// Array of list items
const li_tags = document.querySelectorAll("li.file-link");

// File index span
const file_index = document.getElementById("file-index");
// Previous icon
const previous = document.querySelector(".previous");
// Next icon
const next = document.querySelector(".next");
// Tabs items ul container
const tabs_ul = document.getElementById('tabs-items');
const decisionForm = document.querySelector('.cached');

// Tabs contents div container
const content_div = document.getElementById('tabs-contents');

// Index of the current file
let index = -1;
// Size of decision tabs
let tabs_index = 0;

// Paragraph where to put decision file content
const p_decision = document.getElementById("file-contents");
let text = "";
// Zoom out button
const zoom_out_btn = document.getElementsByClassName("zoom-out");
// Zoom in button
const zoom_in_btn = document.getElementsByClassName("zoom-in");
// Text size input field
const text_size = document.getElementById("text-size");
// Search input field
const searchBar = document.getElementById("text-search");

const goToNext = () => {
  index = (index + 1) % lis.length;
  lis[index].click();
};

const goToPrevious = () => {
  index = (index - 1) % lis.length;
  if (index < 0) index = lis.length - 1;
  lis[index].click();
};

const displyTextFile = (evt) => {
  // Change the index of the current file in the tool pane
  file_index.innerText = lis_content.indexOf(evt.target.innerHTML) + 1;
  // Get selected decision file link
  let link = evt.target.getAttribute("data-link");
  // Style the selected file
  evt.target.classList.add("selected_file");
  // Loop over other li items to unstyle all others (unstyle previously styled items)
  li_tags.forEach((li) => {
    if (li !== evt.target) {
      li.classList.remove("selected_file");
    }
  });
  // Send GET request to server which will handle the requested file url (with file_read function)
  fetch(link)
    .then((response) => response.text())
    .then((data) => {
      // Populate the decision file content to the appropriate p tag
      p_decision.innerText = data;
      p_decision.style.fontSize = "20px";
      text = data;
    });
};

const highlightSearch = (evt) => {
  let regex = evt.target.value;
  console.log(text);
  // Erase all previous highlights if clear is clicked
  if (regex == "") {
    p_decision.innerText = text;
  }
  p_decision.innerHTML = text.replaceAll(
    regex,
    '<span class = "highlighted">' + evt.target.value + "</span>"
  );
};

const zoom_out = () => {
  let a = parseInt(p_decision.style.fontSize.split("p")[0]) - 1;
  p_decision.style.fontSize = String(a) + "px";
};
const zoom_in = () => {
  let a = parseInt(p_decision.style.fontSize.split("p")[0]) + 1;
  p_decision.style.fontSize = String(a) + "px";
};
const set_size = (evt) => {
  let value = evt.target.value;
  if (value < 0) {
    value = -value;
    evt.target.value = value;
  }
  p_decision.style.fontSize = String(value) + "px";
};

const selectTab = evt => {
  // Declare all variables
  let i, tabcontent;
  
  // Get all elements with class="tab-content" and hide them
  tabcontent = document.getElementsByClassName("tab-content");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  
  // Show the current tab, and add an "active" class to the button that opened the tab
  let li = evt.target.closest('li');

  // Delete any previous highlited tabs
  // nodes are the li items of tabs
  let nodes = Array.from(tabs_ul.children);

  for (i = 0; i < nodes.length; i++) {
    // for each li item we remove active class from the included button
    nodes[i].children[0].classList.remove('active');
  }
  // Make the clicked button highlited
  li.children[0].classList.add('active');
  
  // Get the index of the clicked item
  let index = parseInt(nodes.indexOf( li ));
  
  // Display the correspandant tab content
  //console.log(index);
  let selectedTab = document.getElementById('decision-'+ index) || document.getElementById('infos');

  selectedTab.style.display = "block";
 // console.log(content_div.children[index]);
}
// convert html string to HTML node
const htmlToElement = html =>  {
  let template = document.createElement('template');
  html = html.trim(); // Never return a text node of whitespace as the result
  template.innerHTML = html;
  return template.content.firstChild;
}

const htmlToElements = html => {
  let template = document.createElement('template');
  template.innerHTML = html;
  return template.content.childNodes;

}
// create a new demande tab
const addDemande = () => {
  tabs_index ++;
  // Add a new tab
  idx = parseInt(tabs_index);
  let decisionTabTxt = 'demande ' + idx;
  let tabBtn = htmlToElement('<button id="'+idx+'"  onclick="selectTab(event)">'+ decisionTabTxt+'</button>');
  let tabLi  = htmlToElement('<li class="tab-item"></li>');
  tabLi.appendChild(tabBtn);
  tabs_ul.appendChild(tabLi);
  // Add the tab content
  let contentDiv = htmlToElement('<div id="decision-'+idx+'"  class="tab-content"></div>');
  let decisionForm = htmlToElement
  ('<form action="/annotate/" method="POST" enctype="multipart/form-data"></form>');
  //let csrf = htmlToElement('<input type="hidden" name="_csrf" value="{{% csrf_token %}}" />');
  fetch('new_decision_form')
    .then((response) => response.text())
    .then((data) => {
      // Populate the decision file content to the appropriate p tag
      decisionForm.append(htmlToElement(data));
    });
  contentDiv.append(decisionForm);
  content_div.appendChild(contentDiv);
  tabBtn.click();
}

const removeDemande = () => {
  // Get the index of the selected tab
  index = -1;
  // nodes are the li items of tabs
  let nodes = Array.from(tabs_ul.children);
  for (i = 0; i < nodes.length; i++) {
    // for each li item we remove active class from the included button
  if(nodes[i].children[0].classList.contains('active')){
      index = i;
      break;
    }
  }
  if (index == -1 || index == 0) {
    alert('Séléctionnes une demande pour pouvoir supprimer!');
    return;
  }
  //console.log(tabs_ul.childNodes[0]);
  tabs_ul.removeChild(tabs_ul.children[index]);
  content_div.removeChild(content_div.children[index]);
  tabs_index --;
  // tab nodes must be updated
  nodes = Array.from(tabs_ul.children);
  for (let index = 0; index < nodes.length; index++) {
    const tab_btn = nodes[index].children[0];
    if (tab_btn.hasAttribute('id')) {
      tab_btn.id = parseInt(index);
      tab_btn.innerText = 'demande ' + tab_btn.id;
    }
  }

  // content node IDs must be updated
  content_nodes = Array.from(content_div.children);
  for (let i = 0; i < content_nodes.length; i++) {
    if (i !== 0 ) {
      content_nodes[i].id = 'decision-'+parseInt(i);
    }

  }
  
}
let juges = 1;
const addJuge = () => {
  // No more than 10 judjes
  if (juges == 13) return;
  let index_juge = parseInt(juges);
  document.querySelector('#add-juge-'+index_juge).style.display = 'none';
  document.querySelector('#remove-juge-'+index_juge).style.display = 'none';
  juges++;
  index_juge = parseInt(juges);
  let h3 = htmlToElement('<h4>'+index_juge+'.</h4>');
  let titre = htmlToElement('<input placeholder="Titre" type="text" size="10" required>');
  let nom = htmlToElement('<input placeholder="Nom" type="text" size="25" required>');
  let prenom = htmlToElement('<input placeholder="Prénom" type="text" size="25" required>');
  let add = htmlToElement('<img id="add-juge-'+index_juge+'" onclick="addJuge()" src="../static/add_circle-24px.svg" alt="Ajouter juge">');
  let remove = htmlToElement('<img id="remove-juge-'+index_juge+'" onclick="removeJuge(this)" src="../static/remove_circle-24px.svg" alt="Supprimer juge">');
  let jugeDiv = htmlToElement('<div class="juge-'+index_juge+' juge"></div>');
  jugeDiv.appendChild(h3);
  jugeDiv.appendChild(titre);
  jugeDiv.appendChild(nom);
  jugeDiv.appendChild(prenom);
  jugeDiv.appendChild(add);
  jugeDiv.appendChild(remove);
  document.querySelector('.infos-row-3').appendChild(jugeDiv);
}

function removeJuge (e) {
  if (e.id == 'remove-juge-1') return;
  let index = parseInt(juges);
  document.querySelector('.infos-row-3').removeChild(document.querySelector('.juge-'+index));
  juges--;
  index = parseInt(juges);
  document.querySelector('#add-juge-'+index).style.display = 'inline';
  document.querySelector('#remove-juge-'+index).style.display = 'inline';
}

let parties =1;
function addPerson() {
  if (parties == 21) return;
  let index_parties = parseInt(parties);
  document.querySelector('.parties-btns-'+index_parties).style.display = 'none';
  parties++;
  index_parties = parseInt(parties);
  let h4 = htmlToElement('<h4>'+index_parties+'.</h4>');
  let r1 = htmlToElement('<input type="radio" name="physique-morale" value="physique" id="physique-'+index_parties+'">');
  let physiqueLabel = htmlToElement('<label for="physique-'+index_parties+'">Personne Physique</label>');
  let r2 = htmlToElement('<input type="radio" name="physique-morale" value="morale" id="morale-'+index_parties+'">');
  let moraleLabel = htmlToElement('<label for="morale-'+index_parties+'">Personne Morale</label>');
  let add = htmlToElement('<img id="add-person-'+index_parties+'" onclick="addPerson()" src="../static/add_circle-24px.svg" alt="Ajouter personne">');
  let remove = htmlToElement('<img id="remove-person-'+index_parties+'" onclick="removePerson(this)" src="../static/remove_circle-24px.svg" alt="Supprimer personne">');
  let btnDiv = htmlToElement('<div class="parties-btns-'+index_parties+'"></div>');
  r1.addEventListener('change', displayPartieForm);
  r2.addEventListener('change', displayPartieForm);
  btnDiv.appendChild(add);
  btnDiv.appendChild(remove);
  let typeDiv = htmlToElement('<div class="person-type infos-row"></div>');
  typeDiv.appendChild(h4);
  typeDiv.appendChild(r1);
  typeDiv.appendChild(physiqueLabel);
  typeDiv.appendChild(r2);
  typeDiv.appendChild(moraleLabel);
  typeDiv.appendChild(btnDiv);

  let titre = htmlToElement('<input placeholder="Titre" type="text" size="10" required>');
  let nom = htmlToElement('<input placeholder="Nom" type="text" size="25" required>');
  let prenom = htmlToElement('<input placeholder="Prénom" type="text" size="25" required>');
  let infr1 = htmlToElement('<div class="infos-row"></div>');
  infr1.appendChild(titre);
  infr1.appendChild(nom);
  infr1.appendChild(prenom);
  
  let ddn = htmlToElement('<input placeholder="Date de naissance" type="date" required>');
  let adr1 = htmlToElement('<input placeholder="Adresse" type="text" size="45" required>');
  let infr2 = htmlToElement('<div class="infos-row"></div>');
  infr2.appendChild(ddn);
  infr2.appendChild(adr1);
  
  let personPhysique = htmlToElement('<div class="person-physique-'+index_parties+'">');
  personPhysique.appendChild(infr1);
  personPhysique.appendChild(infr2);
  
  
  let entrepriseName = htmlToElement('<input placeholder="Nom d\'entreprise" type="text" size="35" required>');
  let siret = htmlToElement('<input placeholder="Numéro SIRET" type="text" size="35" required>');
  let naf = htmlToElement('<input placeholder="Numéro NAF" type="text" size="25" required>');
  let adr2 = htmlToElement('<input placeholder="Adresse" type="text" size="45" required>');
  let infr3 = htmlToElement('<div class="infos-row"></div>');
  let infr4 = htmlToElement('<div class="infos-row"></div>');
  infr3.appendChild(entrepriseName);
  infr3.appendChild(siret);
  infr4.appendChild(naf);
  infr4.appendChild(adr2);
  let personMorale = htmlToElement('<div class="person-morale-'+index_parties+'">');
  personMorale.appendChild(infr3);
  personMorale.appendChild(infr4);
  
  let partie = htmlToElement('<div class="partie-'+index_parties+' partie"></div>');
  partie.appendChild(typeDiv);
  partie.appendChild(personPhysique);
  partie.appendChild(personMorale);
  document.querySelector('.infos-row-4').appendChild(partie);
}

const displayPartieForm = function() {
  let formType = '.';
  let otherForm = '.';
  if(this.id.startsWith('physique-')){
    formType += 'person-physique-';
    otherForm += 'person-morale-';
  }
  if(this.id.startsWith('morale-')){
    formType += 'person-morale-';
    otherForm += 'person-physique-';
  }
  formType += this.id.split('-')[1];
  otherForm += this.id.split('-')[1];
  document.querySelector(formType).style.display = 'block';
  document.querySelector(otherForm).style.display = 'none';
}

text_size.addEventListener("keyup", set_size);
text_size.addEventListener("change", set_size);
// searchBar.addEventListener("keyup", highlightSearch);
searchBar.addEventListener("search", highlightSearch);

// Convert Node list (of li) to an Array
lis = [...li_tags];
// Construct the lis content array
let lis_content = [];
lis.forEach((li) => lis_content.push(li.innerHTML));

// Attach every li with displayTextFile function
li_tags.forEach((li) => li.addEventListener("click", displyTextFile));
previous.addEventListener("click", goToPrevious);
next.addEventListener("click", goToNext);
document.getElementById('physique-1').addEventListener('change', displayPartieForm);
document.getElementById('morale-1').addEventListener('change', displayPartieForm);
