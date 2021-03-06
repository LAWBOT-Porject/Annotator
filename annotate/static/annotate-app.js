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
const tabs_ul = document.getElementById("tabs-items");
// const decisionForm = document.querySelector(".cached");
let selected_file_name = "";
// Tabs contents div container
const content_div = document.getElementById("tabs-contents");

const jugesNumber = document.getElementById("juges-number"), 
      partiesNumber = document.getElementById("parties-number"),
      avocatsNumber = document.getElementById("avocats-number"), 
      demandsNumber = document.getElementById("demandes-number"),
      decisionFileName = document.getElementById("file-name")
      ;
// Index of the current file
let index = -1;
// Size of decision tabs
let tabs_index = 0;
let selected_tab_index = 0;
// Paragraph where to put decision file content
const p_decision = document.getElementById("file-contents");
let text = "";
// Zoom out button
const zoom_out_btn = document.getElementsByClassName("zoom-out");
// Zoom in button
const zoom_in_btn = document.getElementsByClassName("zoom-in");
// Text size input field
const text_size = document.getElementById("text-size");
// NoPPAC of default demand category
const defaultCategoryNoPPAC = document.getElementById("category-noppac-annotate");
let defaultCategDescript = "";
let defaultNPPAC = "";

if(localStorage.getItem("defaultNPPAC") != null){
  defaultNPPAC          = localStorage.getItem("defaultNPPAC");
  defaultCategDescript = localStorage.getItem("defaultCategDescript");
  if(selected_tab_index != 0 ){
    document.getElementById("nppac-demand-"+selected_tab_index).value = localStorage.getItem("defaultNPPAC");
    document.getElementById("hidden-nppac-demand-"+selected_tab_index).value = localStorage.getItem("defaultNPPAC");
    document.getElementById("descriptionCategorie-"+selected_tab_index).value = localStorage.getItem("defaultCategDescript");
  }
  defaultCategoryNoPPAC.value = defaultNPPAC;
}

defaultCategoryNoPPAC.addEventListener('change', (evt) => {
  if(evt.target.value == "") {
    localStorage.setItem("defaultNPPAC", "");
    localStorage.setItem("defaultCategDescript", "");
    defaultNPPAC  = "";
    defaultCategDescript = "";
    if(selected_tab_index != 0 ){
      document.getElementById("nppac-demand-"+selected_tab_index).value = "";
      document.getElementById("hidden-nppac-demand-"+selected_tab_index).value = "";
      document.getElementById("descriptionCategorie-"+selected_tab_index).value = "";
    }
    return;
  }
  else{
    // let result =  
    fetch("get_default_category", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
      "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
      "X-CSRFToken": getCookieAnnotate("csrftoken"),
    },
    body: JSON.stringify({ nppac: evt.target.value }), //JavaScript object of data to POST
  })
    .then((response) => {
        //window.location.reload();
        return response.json();
    }).then((data) => {
      defaultCategDescript = data["default_categorie"];
      defaultNPPAC = data["nppac"];
      localStorage.setItem("defaultNPPAC", defaultNPPAC);
    localStorage.setItem("defaultCategDescript", defaultCategDescript);
    if(selected_tab_index != 0 ){
      document.getElementById("nppac-demand-"+selected_tab_index).value = defaultNPPAC;
      document.getElementById("hidden-nppac-demand-"+selected_tab_index).value = defaultNPPAC;
      document.getElementById("descriptionCategorie-"+selected_tab_index).value = defaultCategDescript;
    }
      return {"ppac": data["nppac"], "description": defaultCategDescript};
    })
    .catch(err => {
      console.log(err);
      return '';
    })}
    /* if(result){
    defaultCategDescript = result["description"];
    defaultNPPAC = result["ppac"];
  } */

})

function getCookieAnnotate(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const submitAnnotation = () => {
  // /annotate/submit_individual_demande/
  // let form = document.querySelector('form.form-decision');
  // let formBtn = document.querySelector('button[id^="submit-decision-"]');
  // formBtn.click();
  // console.log('Mohamed');
  if (tabs_index > 0 ){
     for (let tab_idx = 1; tab_idx <= tabs_index; tab_idx++) {
      let demandeurs = [], defendeurs = [];
      for (let i = 1; i <= parties; i++) {
        let demandeur = document.getElementById('demande-' +tab_idx +"-partiedemandeur-" +i )
        let defendeur = document.getElementById('demande-' +tab_idx +"-partiedefendeur-" +i)
        demandeurs.push(demandeur);
        defendeurs.push(defendeur);
      } 
      fetch("submit_individual_demande/"+ tab_idx , {
      method: "POST",
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
        "X-CSRFToken": getCookieAnnotate("csrftoken"),
      },
      body: JSON.stringify({ 
        "Rasoul": "Mohamed"
        // file_name: selected_file_name,
        //  demandeurs: demandeurs,
        //  defendeurs: defendeurs,
       }), //JavaScript object of data to POST
    })
      .then((response) => {
        if (response.ok) {
          //window.location.reload();
          return response.json();
        } else throw new Error("Something went wrong");
      }).then((data) => {
        console.log(data);
        return;
      })
      .catch((error) => {
        console.log(error);
        return;
      });
    }
    }
  }
const goToNext = () => {
  index = (index + 1) % lis.length;
  lis[index].click();
};

const goToPrevious = () => {
  index = (index - 1) % lis.length;
  if (index < 0) index = lis.length - 1;
  lis[index].click();
};

let selected_text = "";
const displyTextFile = (evt) => {
  // Change the index of the current file in the tool pane
  file_index.innerText = lis_content.indexOf(evt.target.innerHTML) + 1;
  // Get selected decision file link
  let link = evt.target.getAttribute("data-link");
  let file_name = evt.target.innerText;
  selected_file_name = file_name;
  decisionFileName.value = file_name;
  // Style the selected file
  evt.target.classList.add("selected_file");
  // Loop over other li items to unstyle all others (unstyle previously styled items)
  li_tags.forEach((li) => {
    if (li !== evt.target) {
      li.classList.remove("selected_file");
    }
  });
  // Send GET request to server which will handle the requested file url (with file_read function)
  // fetch(link)
  fetch("read", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
      "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
      "X-CSRFToken": getCookieAnnotate("csrftoken"),
    },
    body: JSON.stringify({ path: link, file_name: file_name }), //JavaScript object of data to POST
  })
    .then((response) => response.text())
    .then((data) => {
      // console.log(data);
      // Populate the decision file content to the appropriate p tag
      parsed = JSON.parse(data);
      document.getElementById("rg").value = parsed.rg;
      document.getElementById("ville").value = parsed.city;
      document.getElementById("juridiction").value = parsed.juridiction;
      p_decision.value = parsed.file;
      document.getElementById('file-content').value = parsed.file;
      p_decision.style.color = "black"; 
      if(parsed.red == true){
        p_decision.style.color = "red";
       }
      p_decision.style.fontSize = "20px";
      p_decision.style["overflow-y"] = "scroll";
      p_decision.style["overflow-x"] = "hidden";
      document.addEventListener("select", function (event) {
        const selection = event.target.value.substring(
          event.target.selectionStart,
          event.target.selectionEnd
        );
        //console.log(`${selection}`);
        selected_text = selection;
      });
      text = data; //['1st'];
    });
};

const highlightSearch = (evt) => {
  let regex = evt.target.value;
  //console.log(text);
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
// Text Size in decision
const set_size = (evt) => {
  let value = evt.target.value;
  if (value < 0) {
    value = -value;
    evt.target.value = value;
  }
  p_decision.style.fontSize = String(value) + "px";
};

const selectTab = (evt) => {
  // Declare all variables
  let i, tabcontent;

  // Get all elements with class="tab-content" and hide them
  tabcontent = document.getElementsByClassName("tab-content");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  let li = evt.target.closest("li");

  // Delete any previous highlited tabs
  // nodes are the li items of tabs
  let nodes = Array.from(tabs_ul.children);

  for (i = 0; i < nodes.length; i++) {
    // for each li item we remove active class from the included button
    nodes[i].children[0].classList.remove("active");
  }
  // Make the clicked button highlited
  li.children[0].classList.add("active");

  // Get the index of the clicked item
  let index = parseInt(nodes.indexOf(li));
  selected_tab_index = nodes.indexOf(li);
/*   if (selected_tab_index != 0){
    document.getElementById("nppac-demand-"+selected_tab_index).value = defaultNPPAC;
    document.getElementById("descriptionCategorie-"+selected_tab_index).value = defaultCategDescript;
  } */
  // Display the correspandant tab content
  //console.log(index);
  let selectedTab =
    document.getElementById("decision-" + index) ||
    document.getElementById("infos");

  selectedTab.style.display = "block";
  // console.log(content_div.children[index]);
};
// convert html string to HTML node
const htmlToElement = (html) => {
  let template = document.createElement("template");
  html = html.trim(); // Never return a text node of whitespace as the result
  template.innerHTML = html;
  return template.content.firstChild;
};

const htmlToElements = (html) => {
  let template = document.createElement("template");
  template.innerHTML = html;
  return template.content.childNodes;
};
// create a new demande tab
const addDemande = () => {
  tabs_index++;
  // Add a new tab
  idx = parseInt(tabs_index);
  let decisionTabTxt = "Demande " + idx;
  let tabBtn = htmlToElement(
    '<button id="' +
      idx +
      '"  onclick="selectTab(event)">' +
      decisionTabTxt +
      "</button>"
  );
  let tabLi = htmlToElement('<li class="tab-item"></li>');
  tabLi.appendChild(tabBtn);
  tabs_ul.appendChild(tabLi);
  // Add the tab content
  let contentDiv = htmlToElement(
    '<div id="decision-' + idx + '"  class="tab-content"></div>'
  );
  let decisionForm = htmlToElement('<div  class="form-decision"></div>');
  // action="#" method="POST"
  // let line1 = htmlToElement('<h2>'+decisionTabTxt+'</h2>');
  // decisionForm.appendChild(line1);

  // Demandeur
  let demandeurs = htmlToElement("<h3>Demandeur(s)</h3>");
  decisionForm.appendChild(demandeurs);
  // Add Parties into demandeur
  let partiesRows = [];
  for (let i = 0; i < parties; i++) {
    // class name contains avocat just to apply css
    let partieContainer = htmlToElement(
      '<div class="avocat-partie infos-row demande-' + idx + '"></div>'
    );
    let partieLbl = htmlToElement(
      '<label style="cursor: pointer;" for="demande-' +idx +"-partiedemandeur-" +(i + 1) +'">Partie ' + (i + 1) + "</label>"
    );
    let partieChkbx = htmlToElement(
      '<input type="checkbox" value="" name="demande-' +idx +"-partiedemandeur-" +(i + 1) +'" id="demande-' +idx +"-partiedemandeur-" +(i + 1) +'" style="cursor:pointer;">'
    );
    partieContainer.appendChild(partieLbl);
    partieContainer.appendChild(partieChkbx);
    partiesRows.push(partieContainer);
    if ((i % 5 == 0 && i != 0) || i == parties - 1) {
      let temp = htmlToElement('<div class="infos-row-avocat"></div>');
      for (let j = 0; j < partiesRows.length; j++) {
        temp.appendChild(partiesRows[j]);
      }
      decisionForm.appendChild(temp);
      partiesRows = [];
    }
  }
  // Defandeur
  let defendeurs = htmlToElement("<h3>Défendeur(s)</h3>");
  decisionForm.appendChild(defendeurs);
  // Add Parties into defandeur
  partiesRows = [];
  for (let i = 0; i < parties; i++) {
    let partieContainer = htmlToElement(
      '<div class="avocat-partie infos-row demande-' + idx + '"></div>'
    );
    let partieLbl = htmlToElement(
      '<label style="cursor: pointer;" for="demande-' +idx +"-partiedefendeur-" +(i + 1) +'">Partie ' + (i + 1) + "</label>"
    );
    let partieChkbx = htmlToElement(
      '<input type="checkbox" value="" name="demande-' +idx +"-partiedefendeur-" +(i + 1) +'" id="demande-' +idx +"-partiedefendeur-" +(i + 1) +'" style="cursor:pointer;">'
    );
    partieContainer.appendChild(partieLbl);
    partieContainer.appendChild(partieChkbx);
    partiesRows.push(partieContainer);
    if ((i % 5 == 0 && i != 0) || i == parties - 1) {
      let temp = htmlToElement('<div class="infos-row-avocat"></div>');
      for (let j = 0; j < partiesRows.length; j++) {
        temp.appendChild(partiesRows[j]);
      }
      decisionForm.appendChild(temp);
      partiesRows = [];
    }
  }
  // Description + Fondement
  let infos1 = htmlToElement('<div class="infos-row"> </div>');
  let demandePPAC = htmlToElement('<input style="background-color: #CCCCCC;" '+
  'placeholder="NPPAC de demande" size="22" disabled id="nppac-demand-'+idx+
  '" value="'+defaultNPPAC+'" name="nppac-demand-'+idx+'">');
  let demandePPACHidden = htmlToElement('<input type="hidden" id="hidden-nppac-demand-'+idx+
  '" value="'+defaultNPPAC+'" name="hidden-nppac-demand-'+idx+'">');
  infos1.appendChild(demandePPAC);
  infos1.appendChild(demandePPACHidden);
  decisionForm.appendChild(infos1);

  infos1 = htmlToElement('<div class="infos-row"> </div>');
  let classSearch = htmlToElement(
    '<label id="class-search-' + idx + '">Rehercher classe</label>'
    );
  let description = htmlToElement(
    '<textarea style="background-color: #CCCCCC;" rows="3" disabled cols="70"  '+
    'name="descriptionCategorie-'+idx+'" id="descriptionCategorie-' +idx +
      '" placeholder="Description" value="'+defaultCategDescript+'"></textarea>'
  );
  description.value = defaultCategDescript;
  //let fondement = htmlToElement('<input type="text" size="25" name="fondement" id="fondement-'+idx+'" placeholder="Fondement">');
  
  infos1.appendChild(description);
  infos1.appendChild(classSearch);
  decisionForm.appendChild(infos1);
  // Chercher classe de demande + resultat recherche
  /* let infos = htmlToElement('<div class="infos-row-class"> </div>');
  infos1 = htmlToElement('<div class="classe-container"> </div>');
  let r1C1 = htmlToElement('<input type="radio" name="classe" value="classe-1" id="classe-1">');
  let c1 = htmlToElement('<label for="classe-1">Classe 1</label>');
  let r2C2 = htmlToElement('<input type="radio" name="classe" value="classe-2" id="classe-2">');
  let c2 = htmlToElement('<label for="classe-2">Classe 2</label>');
  infos1.appendChild(c1);
  infos1.appendChild(r1C1);
  infos.appendChild(infos1);
  infos1 = htmlToElement('<div class="classe-container"> </div>');
  infos1.appendChild(c2);
  infos1.appendChild(r2C2);
  infos.appendChild(infos1); */
  //decisionForm.appendChild(infos);
  // Montant demande
  infos1 = htmlToElement('<div class="infos-row"> </div>');
  let montantDemande = htmlToElement( //size="20"
    '<input type="text" size="60" value="" name="montant-demande-'+idx+'" id="montant-demande-' +
      idx +
      '" placeholder="Montant demandé">'
  );
  /* let uniteDemande = htmlToElement(
    '<input placeholder="Unité" type="text" size="10" value="" name="unite-demande-'+idx+'" id="unite-demande-' +
      idx +
      '" >'
  );
  let quantiteDemande = htmlToElement(
    '<input placeholder="Quantité Demande" type="text" size="30" value="" name="quantite-demande-'+idx+'" id="quantite-demande-' +
      idx +
      '" >'
  ); */
  infos1.appendChild(montantDemande);
  // infos1.appendChild(uniteDemande);
  // infos1.appendChild(quantiteDemande);
  decisionForm.appendChild(infos1);
  // Pretention, Motifs + Dispositifs
  infos1 = htmlToElement('<div class="demande-txtareas"> </div>');
  let pretention = htmlToElement(
    '<textarea rows="3" cols="45" value="" name="pretention-' +idx +'" id="pretention-' +
      idx +
      '" placeholder="Prétention"></textarea>'
  );
  let motifs = htmlToElement(
    '<textarea rows="3" cols="45" value = "" name="motifs-' +
      idx +
      '" id="motifs-' +
      idx +
      '" placeholder="Motifs"></textarea>'
  );
  let dispositifs = htmlToElement(
    '<textarea rows="3" cols="45" value="" name="dispositifs-' +
      idx +
      '" id="dispositifs-' +
      idx +
      '" placeholder="Dispositifs"></textarea>'
  );
  infos1.appendChild(pretention);
  infos1.appendChild(motifs);
  infos1.appendChild(dispositifs);
  decisionForm.appendChild(infos1);
  // Montant resultat
  infos1 = htmlToElement('<div class="infos-row"> </div>');
  let montantResultat = htmlToElement(//size="20"
    '<input type="text" size="60" value="" name="montant-resultat-'+idx+'" id="montant-resultat-' +
      idx +
      '" placeholder="Montant Résultat">'
  );
  /* let uniteResultat = htmlToElement(
    '<input placeholder="Unité" type="text" value="" name="unite-resultat-'+idx+'" size="10" id="unite-resultat-' +
      idx +
      '" >'
  );
  let quantiteResultat = htmlToElement(
    '<input placeholder="Quantité Résultat" type="text" value="" name="quantite-resultat-'+idx+'" size="30" id="quantite-resultat-' +
      idx +
      '" >'
  ); */
  infos1.appendChild(montantResultat);
  // infos1.appendChild(uniteResultat);
  // infos1.appendChild(quantiteResultat);
  decisionForm.appendChild(infos1);
  // Resultat
  let resultat = htmlToElement('<h3 class="infos-row-2">Résultat</h3>');
  infos1 = htmlToElement('<div class="resultat-container"> </div>');

  let r1Acc = htmlToElement(
    '<input type="radio" name="accept-' +
      idx +
      '" value="accept" id="accept-' +
      idx +
      '" style="cursor:pointer;">'
  );
  let accept = htmlToElement(
    '<label for="accept-' + idx + '" style="cursor: pointer;">Acceptée</label>'
  );
  let r2Reject = htmlToElement(
    '<input type="radio" name="reject-' +
      idx +
      '" value="reject" id="reject-' +
      idx +
      '" style="cursor:pointer;">'
  );
  let reject = htmlToElement('<label for="reject-' + idx + '" style="cursor: pointer;">Rejetée</label>');
  decisionForm.appendChild(resultat);
  infos1.appendChild(accept);
  infos1.appendChild(r1Acc);
  infos1.appendChild(reject);
  infos1.appendChild(r2Reject);
  decisionForm.appendChild(infos1);
  infos1 = htmlToElement('<div class="resultat-container"> </div>');
  let mauvaiseContainer = htmlToElement(
    '<div class="mauvaise-container" style="display: flex; justify-content: space-around; align-items: center;"></div>'
  );
  let mauvaise = htmlToElement(
    '<input type="checkbox" value="mauvaise-'+idx+'" name="mauvaise-'+idx+'" id="mauvaise-' + idx + '" style="cursor:pointer;">'
  );
  let mauvaiseLabel = htmlToElement(
    '<label for="mauvaise-' +
      idx +
      '" style="cursor:pointer; margin-left: 1vh; color: red; font-weight: bold;">Contre exemple</label>'
  );
  mauvaiseContainer.appendChild(mauvaise);
  mauvaiseContainer.appendChild(mauvaiseLabel);
  infos1.appendChild(mauvaiseContainer);
  decisionForm.appendChild(infos1);
  /*  <div class="submit-decision-section"
                        style="display: flex; justify-content: space-around; align-items: center;">
                        <div class="corbeille-container"
                            style="display: flex; justify-content: space-around; align-items: center;">
                            <input type="checkbox" name="corbeille" id="corbeille">
                            <label for="corbeille"
                                style="margin-left: 1vh; color: red; font-weight: bold;">Corbeille</label>
                        </div>
                        <button type="submit">Sauvgarder</button>
                    </div> */
  let submit = htmlToElement(
    '<button style="display:none;" type="submit" id="submit-decision-' + idx + '">Sauvgarder</button>'
  );
  //decisionForm.appendChild(submit);
  //let csrf = htmlToElement('<input type="hidden" name="_csrf" value="{{% csrf_token %}}" />');
  // fetch('new_decision_form')
  //   .then((response) => response.text())
  //   .then((data) => {
  //    Populate the decision file content to the appropriate p tag
  //     decisionForm.append(htmlToElement(data));
  //   });

  contentDiv.append(decisionForm);
  content_div.appendChild(contentDiv);
  selectText();
  tabBtn.click();
  demandsNumber.value = tabs_index;
};

const selectText = () => {
  document.querySelectorAll("form input, form textarea").forEach((i) =>
    i.addEventListener("click", function (evt) {
      // console.log("Mohamed 123");
      //console.log(evt.target);
      evt.target.value = selected_text;
      // this.value = selected_text;
    })
  );
};

const removeDemande = () => {
  // Get the index of the selected tab
  index = -1;
  // nodes are the li items of tabs
  let nodes = Array.from(tabs_ul.children);
  for (i = 0; i < nodes.length; i++) {
    // for each li item we remove active class from the included button
    if (nodes[i].children[0].classList.contains("active")) {
      index = i;
      break;
    }
  }
  if (index == -1 || index == 0) {
    alert("Séléctionnes une demande pour pouvoir supprimer!");
    return;
  }
  //console.log(tabs_ul.childNodes[0]);
  tabs_ul.removeChild(tabs_ul.children[index]);
  content_div.removeChild(content_div.children[index]);
  tabs_index--;
  // tab nodes (tab btns) must be updated
  nodes = Array.from(tabs_ul.children);
  for (let index = 0; index < nodes.length; index++) {
    const tab_btn = nodes[index].children[0];
    if (tab_btn.hasAttribute("id")) {
      tab_btn.id = parseInt(index);
      tab_btn.innerText = "Demande " + tab_btn.id;
    }
  }

  // content node IDs must be updated
  content_nodes = Array.from(content_div.children);
  for (let i = 0; i < content_nodes.length; i++) {
    if (i !== 0) {
      content_nodes[i].id = "decision-" + parseInt(i);
      let demandeurs = Array.prototype.slice.call(content_nodes[i].querySelectorAll('input[id*="-partiedemandeur-"]'));
      demandeurs.forEach(demandeur => {
        let id = demandeur.id;
        id = id.split("-");
        id[1] = i;
        id = id.join("-");
        demandeur.id = id;
        demandeur.name = id;
      });
      let defendeurs = Array.prototype.slice.call(content_nodes[i].querySelectorAll('input[id*="-partiedefendeur-"]'));
      defendeurs.forEach(defendeur => {
        let id = defendeur.id;
        id = id.split("-");
        id[1] = i;
        id = id.join("-");
        defendeur.id = id;
        defendeur.name = id;
      });
      
      let nppac = content_nodes[i].querySelector('input[id^="nppac-demand-"]');
      nppac.id = "nppac-demand-"+i;
      nppac.name = "nppac-demand-"+i;

      nppac = content_nodes[i].querySelector('input[id^="hidden-ppac-demand-"]');
      nppac.id = "hidden-nppac-demand-"+i;
      nppac.name = "hidden-nppac-demand-"+i;
      
      let description = content_nodes[i].querySelector('textarea[id^="descriptionCategorie-"]');
      description.id = "descriptionCategorie-"+i;
      description.name = "descriptionCategorie-"+i;

      let searchLbl = content_nodes[i].querySelector('label[id^="class-search-"]');
      searchLbl.id = "class-search-"+i;

      let montantDemande = content_nodes[i].querySelector('input[id^="montant-demande-"]');
      montantDemande.id = "montant-demande-"+i;
      montantDemande.name = "montant-demande-"+i;
      
      let uniteDemande = content_nodes[i].querySelector('input[id^="unite-demande-"]');
      uniteDemande.id = "unite-demande-"+i;
      uniteDemande.name = "unite-demande-"+i;
      
      let quantiteDemande = content_nodes[i].querySelector('input[id^="quantite-demande-"]');
      quantiteDemande.id = "quantite-demande-"+i;
      quantiteDemande.name = "quantite-demande-"+i;
      
      let pretention = content_nodes[i].querySelector('textarea[id^="pretention-"]');
      pretention.id = "pretention-"+i;
      pretention.name = "pretention-"+i;
      
      let motifs = content_nodes[i].querySelector('textarea[id^="motifs-"]');
      motifs.id = "motifs-"+i;
      motifs.name = "motifs-"+i;
      
      let dispos = content_nodes[i].querySelector('textarea[id^="dispositifs-"]');
      dispos.id = "dispositifs-"+i;
      dispos.name = "dispositifs-"+i;
      
      let montantResultat = content_nodes[i].querySelector('input[id^="montant-resultat-"]');
      montantResultat.id = "montant-resultat-"+i;
      montantResultat.name = "montant-resultat-"+i;
      
      let uniteResultat = content_nodes[i].querySelector('input[id^="unite-resultat-"]');
      uniteResultat.id = "unite-resultat-"+i;
      uniteResultat.name = "unite-resultat-"+i;
      
      let quantiteResultat = content_nodes[i].querySelector('input[id^="quantite-resultat-"]');
      quantiteResultat.id = "quantite-resultat-"+i;
      quantiteResultat.name = "quantite-resultat-"+i;
      
      let accept = content_nodes[i].querySelector('input[id^="accept-"]');
      accept.id = "accept-"+i;
      accept.name = "accept-"+i;
      
      let refuse = content_nodes[i].querySelector('input[id^="reject-"]');
      refuse.id = "reject-"+i;
      refuse.name = "reject-"+i;
      
      let mauvaise = content_nodes[i].querySelector('input[id^="mauvaise-"]');
      mauvaise.id = "mauvaise-"+i;
      mauvaise.name = "mauvaise-"+i;
      
      // Array.from(
      //   Array.from(content_nodes[i].children)[0].children
      // )[0].innerText = "Demande " + parseInt(i);
      //console.log(Array.from(Array.from(content_nodes[i].children)[0].children)[0]);
    }
  }

  demandsNumber.value = tabs_index;
  selected_tab_index = 0;
};
let juges = 1;
const addJuge = () => {
  // No more than 10 judjes
  if (juges == 13) return;
  let index_juge = parseInt(juges);
  document.querySelector("#add-juge-" + index_juge).style.display = "none";
  if (!(index_juge === 1)) {
    document.querySelector("#remove-juge-" + index_juge).style.display = "none";
  }
  juges++;
  index_juge = parseInt(juges);
  let h3 = htmlToElement("<h4>" + index_juge + ".</h4>");
  let titre = htmlToElement(
    '<input placeholder="Titre" type="text" size="10" value="" name="juge-'+index_juge+'-titre">'
  );
  let nom = htmlToElement(
    '<input placeholder="Nom" type="text" size="25" value="" name="juge-'+index_juge+'-nom">'
  );
  let prenom = htmlToElement(
    '<input placeholder="Prénom" type="text" size="25" value="" name="juge-'+index_juge+'-prenom">'
  );
  let add = htmlToElement(
    '<img id="add-juge-' +
      index_juge +
      '" onclick="addJuge()" src="../static/add_circle-24px.svg" alt="Ajouter juge" style="cursor:pointer;">'
  );
  let remove = htmlToElement(
    '<img id="remove-juge-' +
      index_juge +
      '" onclick="removeJuge(this)" src="../static/remove_circle-24px.svg" alt="Supprimer juge" style="cursor:pointer;">'
  );
  let jugeDiv = htmlToElement(
    '<div class="juge-' + index_juge + ' juge"></div>'
  );
  jugeDiv.appendChild(h3);
  jugeDiv.appendChild(titre);
  jugeDiv.appendChild(nom);
  jugeDiv.appendChild(prenom);
  jugeDiv.appendChild(add);
  jugeDiv.appendChild(remove);
  document.querySelector(".infos-row-3").appendChild(jugeDiv);
  selectText();
  jugesNumber.value = juges;
};

function removeJuge(e) {
  if (juges == 1) return;
  let index = parseInt(juges);
  document
    .querySelector(".infos-row-3")
    .removeChild(document.querySelector(".juge-" + index));
  juges--;
  index = parseInt(juges);
  document.querySelector("#add-juge-" + index).style.display = "inline";
  if (!(index === 1)) {
    document.querySelector("#remove-juge-" + index).style.display = "inline";
  }
  jugesNumber.value = juges;
}

let parties = 2;
function addPerson() {
  if (parties == 21) return;
  let index_parties = parseInt(parties);
  document.querySelector(".parties-btns-" + index_parties).style.display =
    "none";
  parties++;
  index_parties = parseInt(parties);
  let h4 = htmlToElement("<h4>" + index_parties + ".</h4>");
  let r1 = htmlToElement(
    '<input type="radio" name="physique-morale-' +
      index_parties +
      '" value="physique" id="physique-' +
      index_parties +
      '" style="cursor:pointer;">'
  );
  let physiqueLabel = htmlToElement(
    '<label for="physique-'+index_parties+'" style="cursor:pointer;">Personne Physique</label>'
  );
  let r2 = htmlToElement(
    '<input type="radio" name="physique-morale-' +
      index_parties +
      '" value="morale" id="morale-' +
      index_parties +
      '" style="cursor:pointer;">'
  );
  let moraleLabel = htmlToElement(
    '<label for="morale-' + index_parties + '" style="cursor:pointer;">Personne Morale</label>'
  );
  let add = htmlToElement(
    '<img id="add-person-' +
      index_parties +
      '" onclick="addPerson()" src="../static/add_circle-24px.svg" alt="Ajouter personne" style="cursor:pointer;">'
  );
  let remove = htmlToElement(
    '<img id="remove-person-' +
      index_parties +
      '" onclick="removePerson()" src="../static/remove_circle-24px.svg" alt="Supprimer personne" style="cursor:pointer;">'
  );
  let btnDiv = htmlToElement(
    '<div class="parties-btns-' + index_parties + '"></div>'
  );
  r1.addEventListener("change", displayPartieForm);
  r2.addEventListener("change", displayPartieForm);
  btnDiv.appendChild(add);
  btnDiv.appendChild(remove);
  let typeDiv = htmlToElement('<div class="person-type infos-row"></div>');
  typeDiv.appendChild(h4);
  typeDiv.appendChild(r1);
  typeDiv.appendChild(physiqueLabel);
  typeDiv.appendChild(r2);
  typeDiv.appendChild(moraleLabel);
  typeDiv.appendChild(btnDiv);

  let titre = htmlToElement(
    '<input placeholder="Titre" type="text" size="10" value="" name="partie-'+index_parties+'-titre">'
  );
  let nom = htmlToElement(
    '<input placeholder="Nom" type="text" size="25" value="" name="partie-'+index_parties+'-nom">'
  );
  let prenom = htmlToElement(
    '<input placeholder="Prénom" type="text" size="25" value="" name="partie-'+index_parties+'-prenom">'
  );
  let infr1 = htmlToElement('<div class="infos-row"></div>');
  infr1.appendChild(titre);
  infr1.appendChild(nom);
  infr1.appendChild(prenom);

  let ddn = htmlToElement(
    '<input placeholder="Date de naissance" type="text" size="25" value="" name="partie-'+index_parties+'-dob">'
  );
  let adr1 = htmlToElement(
    '<input placeholder="Adresse" type="text" size="45" value="" name="partie-'+index_parties+'-adr">'
  );
  let infr2 = htmlToElement('<div class="infos-row"></div>');
  infr2.appendChild(ddn);
  infr2.appendChild(adr1);

  let personPhysique = htmlToElement(
    '<div class="person-physique-' + index_parties + '">'
  );
  personPhysique.appendChild(infr1);
  personPhysique.appendChild(infr2);

  let entrepriseName = htmlToElement(
    '<input placeholder="Nom d\'entreprise" type="text" size="35" value=""  name="partie-'+index_parties+'-nom-entreprise">'
  );
  let siret = htmlToElement(
    '<input placeholder="Numéro SIRET" type="text" size="35" value=""  name="partie-'+index_parties+'-siret">'
  );
  let naf = htmlToElement(
    '<input placeholder="Numéro NAF" type="text" size="25" value="" name="partie-'+index_parties+'-naf">'
  );
  let adr2 = htmlToElement(
    '<input placeholder="Adresse" type="text" size="45" value="" name="partie-'+index_parties+'-adr-entreprise">'
  );
  let infr3 = htmlToElement('<div class="infos-row"></div>');
  let infr4 = htmlToElement('<div class="infos-row"></div>');
  infr3.appendChild(entrepriseName);
  infr3.appendChild(siret);
  infr4.appendChild(naf);
  infr4.appendChild(adr2);
  let personMorale = htmlToElement(
    '<div class="person-morale-' + index_parties + '">'
  );
  personMorale.appendChild(infr3);
  personMorale.appendChild(infr4);

  let partie = htmlToElement(
    '<div class="partie-' + index_parties + ' partie"></div>'
  );
  partie.appendChild(typeDiv);
  partie.appendChild(personPhysique);
  partie.appendChild(personMorale);
  document.querySelector(".infos-row-4").appendChild(partie);

  selectText();
  partiesNumber.value = parties;
}
// To display either person or entreprise
const displayPartieForm = function () {
  let formType = ".";
  let otherForm = ".";
  if (this.id.startsWith("physique-")) {
    formType += "person-physique-";
    otherForm += "person-morale-";
    this.checked = true;
  }
  if (this.id.startsWith("morale-")) {
    formType += "person-morale-";
    otherForm += "person-physique-";
    this.checked = true;
  }
  formType += this.id.split("-")[1];
  otherForm += this.id.split("-")[1];
  document.querySelector(formType).style.display = "block";
  document.querySelector(otherForm).style.display = "none";
};

const removePerson = () => {
  if (parties == 2) return;
  let index = parseInt(parties);
  document
    .querySelector(".infos-row-4")
    .removeChild(document.querySelector(".partie-" + index));
  parties--;
  index = parseInt(parties);
  document.querySelector(".parties-btns-" + index).style.display = "inline";
  partiesNumber.value = parties;
};

let avocats = 0;
function addAvocat() {
  avocats++;
  let h4 = htmlToElement("<h4>" + avocats + ".</h4>");
  let titre = htmlToElement(
    '<input placeholder="Titre" type="text" size="5" value="" name="avocat-'+avocats+'-titre" >'
  );
  let prenom = htmlToElement(
    '<input placeholder="Nom" type="text" size="20" value="" name="avocat-'+avocats+'-prenom">'
  );
  let nom = htmlToElement(
    '<input placeholder="Prénom" type="text" size="20" value="" name="avocat-'+avocats+'-nom">'
  );
  let bareau = htmlToElement(
    '<input placeholder="Barreau" type="text" size="20" value="" name="avocat-'+avocats+'-bareau">'
  );
  let infos1 = htmlToElement('<div class="infos-row-avocat"></div>');
  infos1.appendChild(h4);
  infos1.appendChild(titre);
  infos1.appendChild(prenom);
  infos1.appendChild(nom);
  infos1.appendChild(bareau);
  let avocat = htmlToElement(
    '<div class="avocat-' + avocats + ' avocat"></div>'
  );
  avocat.appendChild(infos1);
  let partiesRows = [];
  for (let i = 0; i < parties; i++) {
    let partieContainer = htmlToElement('<div class="avocat-partie"></div>');
    let partieLbl = htmlToElement(
      '<label for="avocat-'+avocats+'-partie-' +(i + 1) +'" style="cursor:pointer;">Partie ' + (i + 1) + "</label>"
    );
    let partieChkbx = htmlToElement(
      '<input type="checkbox" value="avocat-'+avocats+'-partie-' +(i + 1) +'" name="avocat-'+avocats+'-partie-' +(i + 1) +'" id="avocat-'+avocats+'-partie-' +(i + 1) +'" style="cursor:pointer;">'
    );
    partieContainer.appendChild(partieLbl);
    partieContainer.appendChild(partieChkbx);
    partiesRows.push(partieContainer);
    if ((i % 5 == 0 && i != 0) || i == parties - 1) {
      let infos = htmlToElement('<div class="infos-row-avocat"></div>');
      for (let j = 0; j < partiesRows.length; j++) {
        infos.appendChild(partiesRows[j]);
      }
      avocat.appendChild(infos);
      partiesRows = [];
    }
  }
  document.querySelector(".infos-row-5").appendChild(avocat);
  selectText();
  avocatsNumber.value = avocats;
}

function removeAvocat(e) {
  if (avocats == 0) return;
  let toDelete = document.querySelector(".avocat-" + avocats);
  toDelete.parentNode.removeChild(toDelete);
  avocats--;
  avocatsNumber.value = avocats;
}
text_size.addEventListener("keyup", set_size);
text_size.addEventListener("change", set_size);
// searchBar.addEventListener("keyup", highlightSearch);
//searchBar.addEventListener("search", highlightSearch);

// Convert Node list (of li) to an Array
lis = [...li_tags];
// Construct the lis content array
let lis_content = [];
lis.forEach((li) => lis_content.push(li.innerHTML));

// Attach every li with displayTextFile function
li_tags.forEach((li) => li.addEventListener("click", displyTextFile));
previous.addEventListener("click", goToPrevious);
next.addEventListener("click", goToNext);
document
  .getElementById("physique-1")
  .addEventListener("change", displayPartieForm);
document
  .getElementById("morale-1")
  .addEventListener("change", displayPartieForm);
document
  .getElementById("physique-2")
  .addEventListener("change", displayPartieForm);
document
  .getElementById("morale-2")
  .addEventListener("change", displayPartieForm);
selectText();
