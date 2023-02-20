$(document).ready(function () {
  $("#util_project_reset_btn").on("click", function () {
    resetSelection("project");
  });
});
// Highlight on click
function initHighlightButton(id, mode) {
  $("#" + id).on("click", function () {
    message = getSelections();
    message["mode"] = mode;
    message["id"] = id;
    message["text"] = document.getElementById(id).value;
    if ($("#util_use_highlight").is(":checked")) {
      message["highlight"] = true;
    } else {
      message["highlight"] = false;
    }
    // message["color"] = $("#util_highlight_color").colorbox.value;
    utilSocket.emit("highlight", message);
  });
}
