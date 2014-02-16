'use strict';
var decimalSeparator = localizedNum[1];
function localizeNum(num) {
   return num.toString().replace(".", decimalSeparator);
}

var ajaxUploaderCompatible = (function() {
   // Test for FileReader
   if (!window.FileReader) {
      return false;
   }

   // Test for AJAX2
   var xhr = new XMLHttpRequest();
   if (!xhr.upload) {
      return false;
   }

   // Everything OK, this browser is compatible
   return true;
})();

function $id(id) {
   var element = document.getElementById(id);
   if (element) {
      return element;
   } else {
      throw "no element with id \"" + id + "\"";
   } 
}

// Global variables
var dropBox = $id("form_container"); // where files are drop
var file; // file to upload
var xhr; // AJAX upload request
var ceHack; // Firefox contenteditable hack
var disableCeHack = false; // Avoid the hack if possible

function setPage(name) {
   $id("page_select").style.display = "none";
   $id("page_confirm").style.display = "none";

   if (name == "select") {
      $id("page_"+name).style.display = "block";
   } else {
      $id("subpage_confirm").style.display = "none";
      $id("subpage_progress").style.display = "none";
      $id("subpage_finished").style.display = "none";
      $id("subpage_error").style.display = "none";

      // Show subpage
      if (name == "confirm") {
         $id("subpage_confirm").style.display = "block";
      } else if (name == "progress") {
         $id("subpage_progress").style.display = "block";
      } else if (name == "finished") {
         $id("subpage_finished").style.display = "block";
      } else if (name == "error") {
         $id("subpage_error").style.display = "block";
      }

      // Show page
      $id("page_confirm").style.display = "block";
   }
}

function initAjaxUploader() {
   $id("form_container").className = "ajax";

   // Create a hidden file input
   var fileHack = document.createElement("input");
   fileHack.setAttribute("type", "file");
   fileHack.setAttribute("id", "file_hack");
   // Internet Explorer 10 needs a bit more of tweaking in order for show the
   // file dialog on a single click.
   if (window.navigator.appName == "Microsoft Internet Explorer") {
      fileHack.style.fontSize = "200px";
   }
   fileHack.addEventListener("change", handleFileSelect);
   $id("page_select").appendChild(fileHack);

   // Focus file selector so it can be opened with Return key
   fileHack.focus();

   // Bind drag and drop events
   dropBox.addEventListener("dragover", function(e) {
      e.preventDefault();
      e.stopPropagation();
      dropBox.className = "ajax hover";
   }, false);
   dropBox.addEventListener("dragleave", function() {
      dropBox.className = "ajax";
   }, false);
   dropBox.addEventListener("drop", handleDrop, false);

   // Bind paste events
   initPasteHandler();

   // Bind buttons
   $id("upload_button").addEventListener("click", startUpload, false);
   $id("confirm_cancel").addEventListener("click", function() {
      setPage("select"); }, false);
   $id("cancel_upload").addEventListener("click", cancelUpload, false);
   $id("store_more_button").addEventListener("click", storeMore, false);
   $id("retry_button").addEventListener("click", function() {
      setPage("confirm"); }, false);
}

function handleFileSelect(e) {
   // Called when the user picks a file in the file dialog

   var files = e.target.files;
   if (files.length == 1) {
      confirmFile(files[0]);
   }
}

function handleDrop(e) {
   // Prevent the browser from taking the default action (leaving the page)
   e.stopPropagation();
   e.preventDefault();

   // Remove .hover class
   dropBox.className = "ajax";

   var files = e.dataTransfer.files;
   if (files.length == 1) {
      confirmFile(files[0]);
   }
}

function fileIsPicture(file) {
   var types = [
      "image/png",
      "image/jpeg",
      "image/gif"
   ];
   for (var i=0; i < types.length; i++) {
      if (file.type == types[i]) {
         return true;
      }
   }
   return false;
}

function humanSize(byteSize) {
   var KiB = 1024;
   var MiB = 1024 * 1024;
   var GiB = 1024 * 1024 * 1024;
   var prec = 1;

   if (byteSize < KiB) {
      return byteSize + " bytes";
   } else if (byteSize < MiB) {
      return (byteSize / KiB).toFixed(prec) + " KiB";
   } else if (byteSize < GiB) {
      return (byteSize / MiB).toFixed(prec) + " MiB";
   } else {
      return (byteSize / GiB).toFixed(prec) + " GiB";
   }
}

function confirmFile(new_file) {
   file = new_file; // Make global
   $id("file_name").textContent = file.name;
   $id("file_size").textContent = localizeNum(humanSize(file.size));

   var imagePane = $id("image_pane");
   imagePane.innerHTML = "";
   if (fileIsPicture(file)) {
      imagePane.style.visibility = "visible";
      $id("page_confirm").className = "";

      var reader = new FileReader();
      reader.onload = function() {
         var img = document.createElement("img");
         img.setAttribute("src", reader.result);
         imagePane.appendChild(img);
      };
      reader.readAsDataURL(file);
   } else {
      imagePane.style.visibility = "hidden";
      $id("page_confirm").className = "no_image";
   }

   setPage("confirm");
}

function setProgress(completed, total) {
   var ratio = completed / total;
   $id("percent").textContent = (ratio * 100).toFixed(0) + " %";
   $id("filled_area").style.width = Math.min(100, ratio * 100) + "%";
}

function uploadProgress(e) {
   setProgress(e.loaded, file.size);
}

function startUpload() {
   setProgress(0, 100);
   setPage("progress");

   var formData = new FormData();
   formData.append("expires_in", $id("ajax_expires_in").value);
   formData.append("file", file);
   // If this is not a real File object, but a Blob object with a name
   // property, append a file name override field, as the browser will send
   // filename=blob.
   if (!(file instanceof File)) {
      formData.append("file_name_override", file.name);
   }

   xhr = new XMLHttpRequest();

   xhr.upload.onprogress = uploadProgress;
   xhr.onload = uploadComplete;
   xhr.error = uploadFailed;

   xhr.open("POST", "/api/v1/", true);
   //xhr.open("POST", "https://lasana.rufian.eu/api/v1/", true);
   xhr.send(formData);
}

function uploadComplete(e) {
   if (this.status == 200) {
      var data = JSON.parse(this.response);
      var urlField = $id("lasagna_url_field");
      urlField.value = data.url;
      setPage("finished");

      urlField.setSelectionRange(0, urlField.value.length);
      urlField.select();
   } else {
      uploadFailed();
   }
}

function cancelUpload() {
   xhr.abort();
   setPage("confirm");
}

function uploadFailed(e) {
   setPage("error");
}

function storeMore() {
   setPage("select");
}

function initPasteHandler() {
   // For Chrome
   document.addEventListener("paste", pasteHandler, false);

   // The rest of this function is the contenteditable hack for Firefox

   // Create a focusable but mostly hidden contenteditable div
   ceHack = document.createElement("div");
   ceHack.setAttribute("contenteditable", "true");
   ceHack.setAttribute("tabindex", "-1");
   ceHack.style.opacity = "0";
   ceHack.style.position = "absolute";
   ceHack.style.left = "-10000px";
   ceHack.style.top = "-10000px";
   document.getElementsByTagName("body")[0].appendChild(ceHack);

   // Focus ceHack on <C-v>
   window.addEventListener("keydown", function(e) {
      if (!disableCeHack && (e.ctrlKey || e.metaKey) && e.keyCode == 86) {
         ceHack.focus();
      }
   });

   // Listen for changes in ceHack
   var observer = new MutationObserver(firefoxPasteHandler);
   observer.observe(ceHack, {childList: true});
}

function pad(number, positions) {
   var numStr = new String(number);
   for (var i = positions - numStr.length; i > 0; i--) {
      numStr = "0" + numStr;
   }
   return numStr;
}

function defaultName(type) {
   var date = new Date();
   var dateStr = date.getFullYear() + "-" + 
                  pad(date.getMonth() + 1, 2) + "-" +
                  pad(date.getDate(), 2) + "-" +
                  pad(date.getHours(), 2) + "-" +
                  pad(date.getMinutes(), 2) + "-" +
                  pad(date.getSeconds(), 2);
   var extensions = {
      "image/png": "png",
      "image/jpeg": "jpeg",
      "image/gif": "gif",
      "text/plain": "txt"
   }

   return dateStr + ("." + extensions[type] || "");
}

function pasteHandler(e) {
   var items = e.clipboardData.items;
   if (!items) return; // items is undefined in Firefox :(
   var file = null;
   for (var i = 0; i < items.length; i++) {
      var item = items[i];
      if (item.kind == "file") {
         file = item.getAsFile();
         break;
      }
   }
   if (file) {
      disableCeHack = true;
      file.name = file.name || defaultName(file.type);
      confirmFile(file);
   }
}

// http://stackoverflow.com/a/14930686/1777162
function dataURItoBlob(dataURI) {
   var byteString, 
       mimestring 

   if(dataURI.split(',')[0].indexOf('base64') !== -1 ) {
       byteString = atob(dataURI.split(',')[1])
   } else {
       byteString = decodeURI(dataURI.split(',')[1])
   }

   mimestring = dataURI.split(',')[0].split(':')[1].split(';')[0]

   var content = new Array();
   for (var i = 0; i < byteString.length; i++) {
       content[i] = byteString.charCodeAt(i)
   }

   return new Blob([new Uint8Array(content)], {type: mimestring});
}

function firefoxPasteHandler() {
   if (!disableCeHack) {
      var images = ceHack.getElementsByTagName("img");
      if (images.length > 0) {
         var img = images[0];
         var src = img.getAttribute("src");
         var blob;
         if (src.match(/https?:/)) {
            alert(noBrowserImagesError);
         } else if (src.lastIndexOf("data:", 0) === 0) {
            blob = dataURItoBlob(src);

            // A File object is a Blob plus a file name, but I'm not aware of
            // any way to convert a Blob in a File object with name.

            // File constructor should be able to do this, but it raises a
            // security exception on Firefox.

            // Instead, I'll put a name property in the Blob object itself.
            // Later, startUpload will detect that it does not have a real File
            // object, read this property and add an override field for the
            // file name.
            blob.name = defaultName(blob.type);
            confirmFile(blob);
         }
      }
   }
   // Don't leave old elements in the ceHack
   ceHack.innerHTML = "";
}

if (ajaxUploaderCompatible) {
   initAjaxUploader();
}
