// Builds each .shortcode-gallery from its JSON file, then wires up lightGallery.
// Item fields: src (full image), thumb (thumbnail), alt, download.
function createGalleryItemElement(item) {
  var a = document.createElement("a");
  var img = document.createElement("img");

  a.setAttribute("href", item.src);
  if (item.download) a.setAttribute("data-download", item.download);
  if (item.title) a.setAttribute("title", item.title);
  if (item.subHtml) a.setAttribute("data-sub-html", item.subHtml);
  img.setAttribute("src", item.thumb || item.src);
  img.setAttribute("alt", item.alt || "");
  img.setAttribute("loading", "lazy");

  a.appendChild(img);
  return a;
}

function createGallery(elId, data) {
  var lightGalleryOptions = data.lightGalleryOptions || {};
  lightGalleryOptions.plugins = [lgZoom, lgThumbnail];
  lightGalleryOptions.licenseKey = "0000-0000-000-0001";

  var el = document.getElementById(elId);
  el.innerHTML = "";
  data.items.forEach(function (item) {
    el.appendChild(createGalleryItemElement(item));
  });

  $("#" + elId)
    .justifiedGallery(data.justifiedGalleryOptions || {})
    .on("jg.complete", function () {
      lightGallery(el, lightGalleryOptions);
    });
}

$(document).ready(function () {
  $(".shortcode-gallery").each(function () {
    var elId = this.id;
    $.getJSON($(this).attr("data"), function (data) {
      createGallery(elId, data);
    });
  });
});
