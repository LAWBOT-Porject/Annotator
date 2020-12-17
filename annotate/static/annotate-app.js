/* Author : Sid Ali MAHMOUDI @ 20/11/2020 */

//Array of list items
const li_tags = document.querySelectorAll('li.file-link');

// File index span
const file_index = document.getElementById('file-index');

// Paragraph where to put decision file content
const p_decision = document.getElementById('file-contents');

const displyTextFile = (evt) => {
  // Change the index of the current file in the tool pane
  file_index.innerText = lis_content.indexOf(evt.target.innerHTML) + 1;
  // Get selected decision file link
  let link = evt.target.getAttribute("data-link");
  // Style the selected file
  evt.target.classList.add('selected_file');
  // Loop over other li items to unstyle all others (unstyle previously styled items)
  li_tags.forEach(li => {
    if(li !== evt.target) {
      li.classList.remove('selected_file');
    }
  });
  // Send GET request to server which will handle the requested file url (with file_read function)
  fetch(link)
  .then(response => response.text())
  .then(data => {
    // Populate the decision file content to the appropriate p tag
    p_decision.innerText = data;
  });  
}
// Convert Node list (of li) to an Array
lis = [...li_tags]
// Constructing the lis content array
let lis_content = []
lis.forEach( li => lis_content.push(li.innerHTML));

// Attach every li with displayTextFile function
li_tags.forEach( li => li.addEventListener('click', displyTextFile));
