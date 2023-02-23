utilSocket = io.connect(
  "http://" + location.hostname + ":" + location.port + "/Util"
);
// receive status
utilSocket.on("status", function (data) {
  button = document.getElementById(data.id);

  button.value = data.text;
  button.disabled = false;
  sm = data.sm;
  if (sm != undefined) {
    setStatus(data.status, sm, data.message);
  }
  if (data.id == "util_store_highlight_btn") {
    updateProjectList(data.projectName);
  }
  $("#" + data.id).removeClass("loadingButton");
});
