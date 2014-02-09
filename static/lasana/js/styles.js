'use strict';

var userStyle = document.getElementById("user_style");
var styleList = document.getElementById("set_your_style");
var currentStyleName;

function styleNameFromCssUrl(url) {
   return url.match(/([^/.]+)\.css$/)[1];
}
function styleNameFromSetStyleUrl(url) {
   return url.match(/style=([^=]+)$/)[1];
}
function styleUrl(name) {
   return styleRoot + name + ".css";
}
function setStyleUrl(name) {
   return setStyleUrlBase + name;
}

function ajaxizeStyles() {
   // Ajaxize links
   var styles = styleList.getElementsByTagName("a");
   for (var i = 0; i < styles.length; i++) {
      var style = styles[i];
      style.addEventListener("click", changeStyle, false);
   }

   // Get current style
   currentStyleName = styleNameFromCssUrl(userStyle.getAttribute("href"));
}

function changeStyle(e) {
   e.preventDefault();
   
   // Put a link around the older style
   var styles = styleList.getElementsByTagName("li");
   for (var i = 0; i < styles.length; i++) {
      var style = styles[i];
      if (style.textContent.toLowerCase().trim() == currentStyleName) {
         // This is the current style
         style.innerHTML = '<a href="' + setStyleUrl(currentStyleName) +
            '">' + style.innerHTML + '</a>';
         // Ajaxize the new link
         var a = style.getElementsByTagName("a")[0];
         a.addEventListener("click", changeStyle, false);
      }
   }

   // Set this stylesheet
   currentStyleName = styleNameFromSetStyleUrl(this.getAttribute("href"));
   userStyle.setAttribute("href", styleUrl(currentStyleName));

   // Ping the server so the style is set as default
   var xhr = new XMLHttpRequest();
   xhr.open("GET", this.getAttribute("href"));
   xhr.send();

   // Remove the link of the new style
   var li = this.parentNode;
   li.innerHTML = li.textContent;
}

window.addEventListener("load", ajaxizeStyles, false);
