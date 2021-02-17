let directory = "",
  selected_dir_path = "",
  selected_dir_move = "",
  selected_dir_path_move = "";
let keys = 1;
const htmlToElementOrganize = (html) => {
  let template = document.createElement("template");
  html = html.trim(); // Never return a text node of whitespace as the result
  template.innerHTML = html;
  return template.content.firstChild;
};

function loadHome() {
  document.querySelector(".search-result-hider").style.display = "none";
  document.querySelector(".research-result-container").style.display = "none";
  let a = document.getElementById("home-dir").alt;
  let myUl = document.getElementById("myUL");
  myUl.innerHTML = a;
  myUl.style.fontSize = "1.25rem";
  myUl.style.display = "block";
  let levels = document.querySelectorAll('li[class^="level-"]');
  let carets = document.querySelectorAll('span[class^="caret"]');
  levels = [...levels];
  carets = [...carets];
  levels.forEach((item) => {
    arr = item.className.split("-");
    if (arr.indexOf("level") == 0) {
      item.style.paddingLeft = 15 * parseInt(arr[1]) + "px";
    }
  });
  let icons_container = document.querySelector(".dir-manager");
  carets.forEach((item) => {
    item.addEventListener("click", (e) => {
      carets.forEach((i) => {
        i.style.backgroundColor = "";
      });
      e.target.style.backgroundColor = "#3f7cac";
      directory = e.target.innerText;
      document.getElementById("annotate-organize").href =
        "/annotate/" + directory;
      selected_dir_path = e.target.dataset.path;
      icons_container.style.visibility = "visible";
    });
  });
  let toggler = document.getElementsByClassName("caret");
  let i;

  for (i = 0; i < toggler.length; i++) {
    toggler[i].addEventListener("click", function () {
      this.parentElement.querySelector(".nested").classList.toggle("active");
      this.classList.toggle("caret-down");
    });
  }
}

const addDir = () => {
  let new_dir = prompt("Nom du nouveau répertoire:", "Nouveau_répertoire");
  if (new_dir == null || new_dir == undefined) {
    return;
  } else {
    fetch("create_new_directory_annotator", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ path: selected_dir_path + "/" + new_dir }), //JavaScript object of data to POST
    })
      .then((response) => {
        if (response.ok) {
          window.location.reload();
        } else throw new Error("Something went wrong");
      })
      .catch((error) => {
        console.log(error);
        return;
      });
  }
};

const addKey = () => {
  //document.querySelectorAll("#key-word-type-1 option").disabled = false;
  keys++;
  keys_str = parseInt(keys);
  let container = htmlToElementOrganize('<div class="key-row-' + keys_str + '">');
  let key = htmlToElementOrganize(
    '<input id="key-' +
      keys_str +
      '" type="text" size="40" placeholder="mot clé" required>'
  );
  container.appendChild(key);
  let options = htmlToElementOrganize(
    '<select name="key-word-type-' +
      keys_str +
      '" id="key-word-type-' +
      keys_str +
      '" title="Choisir un opérateur logique" ><option value="and" >Et</option><option value="or">Ou</option> <option value="except">Sauf</option></select>'
  );
  container.appendChild(options);
  let addIcon = htmlToElementOrganize(
    '<img id="add-key-' +
      keys_str +
      '" onclick="addKey()" src="../static/add_circle-24px.svg" alt="Add key word" title="Ajouter un mot clé">'
  );
  let deleteIcon = htmlToElementOrganize(
    '<img id="delete-key-' +
      keys_str +
      '" onclick="deleteKey()" src="../static/remove_circle-24px.svg" alt="Delete key word" title="Supprimer un mot clé">'
  );
  let twoIconsContainer = htmlToElementOrganize(
    '<div class="add-remove-keyword-' + keys_str + '"> </div>'
  );
  twoIconsContainer.appendChild(addIcon);
  twoIconsContainer.appendChild(deleteIcon);
  container.appendChild(twoIconsContainer);
  document.querySelector(".reaserch-keys-container").appendChild(container);
  document.querySelector(
    ".add-remove-keyword-" + parseInt(keys - 1)
  ).style.display = "none";
};

const deleteKey = () => {
  document
    .querySelector(".reaserch-keys-container")
    .removeChild(document.querySelector(".key-row-" + parseInt(keys)));
  keys--;
  keys_str = parseInt(keys);
  document.querySelector(".add-remove-keyword-" + keys_str).style.display =
    "flex";
};

const searchKeyWord = () => {
  let keyWords = [],
    operators = [];

  for (let i = 1; i <= keys; i++) {
    // Verify if any field is empty
    let keyWord = document.getElementById("key-" + i).value;
    if (keyWord == "") {
      alert("Veuillez remplir tous les inputs SVP !");
      return;
    } else {
      // console.log(`${keyWord} ${i}`);
      keyWords.push(keyWord);
      operators.push(document.getElementById("key-word-type-" + i).value);
    }
  }
  fetch("search_key_words", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
      "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ keys: keyWords, ops: operators }), //JavaScript object of data to POST
  })
    .then((response) => {
      //window.location.reload();
      return response.json();
    })
    .then((data) => {
      let bodyContainer = document.querySelector(".search-result-hider");
      bodyContainer.style.display = "flex";
      bodyContainer.style["justify-content"] = "space-between";
      bodyContainer.style["overflow"] = "auto";
      // Where we have move button and all files checkbox
      let resultContainer = document.querySelector(
        ".research-result-container"
      );
      resultContainer.style.display = "flex";
      resultContainer.style["justify-content"] = "space-between";
      resultContainer.style["align-items"] = "center";
      resultContainer.style["padding"] = "5px";
      document.querySelector("#myUL").style.display = "none";
      let dirs_only_html = document.getElementById("dirs-only").name;
      let dirs_only_ul = document.getElementById("dirs-ul");
      // console.log(dirs_only_html);
      dirs_only_ul.innerHTML = dirs_only_html;
      dirs_only_ul.style.fontSize = "1.25rem";

      let levels = document.querySelectorAll('li[class^="level-"]');
      let carets = document.querySelectorAll('span[class^="caret"]');
      levels = [...levels];
      carets = [...carets];
      levels.forEach((item) => {
        arr = item.className.split("-");
        if (arr.indexOf("level") == 0) {
          item.style.paddingLeft = 15 * parseInt(arr[1]) + "px";
        }
      });
      // let icons_container = document.querySelector(".dir-manager");
      carets.forEach((item) => {
        item.addEventListener("click", (e) => {
          carets.forEach((i) => {
            i.style.backgroundColor = "";
          });
          e.target.style.backgroundColor = "#3f7cac";
          selected_dir_move = e.target.innerText;
          selected_dir_path_move = e.target.dataset.path;
          // icons_container.style.visibility = "visible";
        });
      });
      let toggler = document.getElementsByClassName("caret");
      let i;

      for (i = 0; i < toggler.length; i++) {
        toggler[i].addEventListener("click", function () {
          this.parentElement
            .querySelector(".nested")
            .classList.toggle("active");
          this.classList.toggle("caret-down");
        });
      }
      let files = data["file_names"],
        file_paths = data["file_paths"];

      let files_ul = document.getElementById("files-result-ul");
      Array.from(files_ul.children).forEach((item) =>
        files_ul.removeChild(item)
      );
      // files_ul.style["overflow"] = "auto";
      for (let index = 0; index < files.length; index++) {
        let containerDiv = htmlToElementOrganize(
          '<div style = "display: flex" class="file-element-' +
            index +
            '"></div>'
        );
        let file_li = htmlToElementOrganize(
          '<label style="cursor: pointer" id="file-' +
            index +
            '" data-path="' +
            file_paths[index] +
            '" for="file-check-' +
            index +
            '">' +
            files[index] +
            "</label>"
        );
        let check = htmlToElementOrganize(
          '<input id="file-check-' +
            index +
            '" type="checkbox" value="' +
            file_paths[index] +
            '">'
        );
        containerDiv.appendChild(check);
        containerDiv.appendChild(file_li);
        files_ul.appendChild(containerDiv);
      }
      document.getElementById("all-files").addEventListener("change", (evt) => {
        let filesNumber = Array.from(files_ul.children).length;
        if (evt.target.checked) {
          for (let index = 0; index < filesNumber; index++) {
            document.getElementById("file-check-" + index).checked = true;
          }
        } else {
          for (let index = 0; index < filesNumber; index++) {
            document.getElementById("file-check-" + index).checked = false;
          }
        }
      });
      // console.log(data["file_names"]);
      // console.log(data["file_paths"]);
      //loadHome();
    })
    .catch((error) => {
      console.log(`Here is the error: ${error}`);
      return;
    });
};

const moveFiles = () => {
  // console.log(selected_dir_move);
  // console.log(selected_dir_path_move);
  let filesNumber = Array.from(
    document.getElementById("files-result-ul").children
  ).length;
  let fileNames = [],
    filePaths = [];
  // Get selected file names with their paths
  for (let i = 0; i < filesNumber; i++) {
    let li = document.getElementById("file-" + i);
    if (document.getElementById("file-check-" + i).checked) {
      fileNames.push(li.innerText);
      filePaths.push(li.dataset.path);
    }
  }
  // console.log(fileNames);
  // console.log(filePaths);

  fetch("move_files", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
      "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      paths: filePaths,
      names: fileNames,
      targetDir: selected_dir_path_move,
    }), //JavaScript object of data to POST
  })
    .then((response) => {
      window.location.reload();
      return response.json();
    })
    .then((data) => console.log(data["response"]))
    .catch((error) => {
      console.log(error);
    });
};
// get django app attribute like csrftoken
function getCookie(name) {
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
