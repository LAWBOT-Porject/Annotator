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
  /* for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  } */
  
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
  let index = nodes.indexOf( li );
  
  // Display the correspandant tab content
  //console.log(index);
  content_div.children[index].style.display = "block";
  console.log(content_div.children[index]);
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
  let contentDiv = htmlToElement('<div class="tab-content"></div>');
  /* let contentP = htmlToElement('<p>contenu de demande ' + idx + '</p>');
  contentDiv.appendChild(contentP); */
  let decision = htmlToElements(decisionForm);
  //contentDiv.append(Array.from(decision));
  decisionForm.classList.remove('cached');
  //console.log(decisionForm);
  //content_div.append(decisionForm);
  contentDiv.append(decisionForm);
  //console.log('here6');
  //contentDiv.style.display = 'none';
  console.log('fin')
  content_div.appendChild(contentDiv);
  
  tabBtn.click();
  //console.log(decisionForm);
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

  // content nodes can be updated eventually
  content_nodes = Array.from(content_div.children);
  for (let index = 0; index < content_nodes.length; index++) {
    if (!content_nodes[index].hasAttribute('id')) {
      const content = content_nodes[index].children[0];
      content.innerText = 'contenu de demande ' + parseInt(index);
    }
  }
  
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
