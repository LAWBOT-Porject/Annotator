/* Author : Sid Ali MAHMOUDI @ 20/11/2020 */

// Array of list items
const li_tags = document.querySelectorAll("li.file-link");

// File index span
const file_index = document.getElementById("file-index");
// Previous icon
const previous = document.querySelector(".previous");
// Next icon
const next = document.querySelector(".next");
// Index of the current file
let index = -1;

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

function selectTab(evt) {
  // Declare all variables
  let i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tab-content");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  /* tablinks = document.getElementsByClassName("tab-item");
  for (i = 0; i < tablinks.length; i++) {
    console.log(tablinks[i].className);
    tablinks[i].classList.remove('active');
  } */
  
  // Show the current tab, and add an "active" class to the button that opened the tab
  let li = evt.target.closest('li');
  // Delete any previous highlited tabs
  let tabs_ul = document.getElementById('tabs-items');
  // nodes are the li items
  let nodes = Array.from( tabs_ul.children );
  for (i = 0; i < nodes.length; i++) {
    // for each li item we remove active class from the included button
    nodes[i].children[0].classList.remove('active');
  }
  // Make the clicked button highlited
  li.children[0].classList.add('active');
  
  // Get the index of the clicked item
  let index = nodes.indexOf( li );
  let content_div = document.getElementById('tabs-contents');
  // Display the correspandant tab content
  content_div.children[index].style.display = "block";
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
