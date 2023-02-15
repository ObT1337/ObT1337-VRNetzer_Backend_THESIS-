utilSocket = io.connect(
  "http://" + location.hostname + ":" + location.port + "/Util"
);
utilSocket.emit("getSelection");
utilSocket.on("selection", function (data) {
  sessiondata["selected"] = data;
});

$(document).ready(function () {
  if (pdata.selections.layout) {
    $("#layouts").val(pdata.selections.layout);
    $("#layouts").selectmenu("refresh");
  }
  if (pdata.selections.layoutRGB) {
    $("#nodecolors").val(pdata.selections.layoutRGB);
    $("#nodecolors").selectmenu("refresh");
  }
  if (pdata.selections.linkl) {
    $("#links").val(pdata.selections.linkl);
    $("#links").selectmenu("refresh");
  }
  if (pdata.selections.linkRGB) {
    $("#linkcolors").val(pdata.selections.linkRGB);
    $("#linkcolors").selectmenu("refresh");
  }
  if (pdata.selections.main_tab) {
    console.log("ACTIVE TAB", pdata.selections.main_tab);
    $("#tabs").tabs("option", "active", pdata.selections.main_tab);
  }
  $("#util_highlight_selection").click(function () {
    button = document.getElementById("util_highlight_selection");
    button.value = "";
    button.disabled = true;
    message = getSelections();
    $("#util_highlight_selection").addClass("loadingButton");
    utilSocket.emit("highlight", message);
  });
  $("#util_reset_selection").click(function () {
    socket.emit("ex", { id: "reset", fn: "" });
    message = getSelections();
    utilSocket.emit("reset", message);
  });
  // Turn of the Highlight button on other clients
  utilSocket.on("highlight", function (data) {
    button = document.getElementById("util_highlight_selection");
    button.value = "";
    button.disabled = true;
    $("#util_highlight_selection").addClass("loadingButton");
  });

  utilSocket.on("status", function (data) {
    console.log(data["message"]);
    button = document.getElementById("util_highlight_selection");
    button.value = "Highlight Selection";
    button.disabled = false;
    if (data["status"] == "error") {
      $("#analytic_highlight_sm").css("color", "red");
    } else {
      $("#analytic_highlight_sm").css("color", "green");
    }
    $("#util_highlight_selection").removeClass("loadingButton");
    $("#analytic_highlight_sm").text(data["message"]);
    $("#analytic_highlight_sm").css("opacity", "1");
    setTimeout(function () {
      $("#analytic_highlight_sm").css("opacity", "0");
    }, 5000);
  });
});

function getSelections() {
  message = {
    layout: $("#layouts").val(),
    layoutRGB: $("#nodecolors").val(),
    linkl: $("#links").val(),
    linkRGB: $("#linkcolors").val(),
    main_tab: $("#tabs").tabs("option", "active"),
  };
  return message;
}
