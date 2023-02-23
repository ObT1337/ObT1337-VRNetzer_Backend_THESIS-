var node_annotations = {};
var link_annotations = {};
$(document).ready(function () {
  // Init dropdown
  node_annotations = {
    "Annotation 1": { dtype: "str", option: ["a", "b", "c"] },
  };
  link_annotations = {
    "Annotation 1": { dtype: "str", option: ["a", "b", "c"] },
  };
  document.getElementById("util_node_annot").style.visibility = "hidden";
  document.getElementById("util_link_annot").style.visibility = "hidden";
  initDropdown(
    "util_node_select",
    Object.keys(node_annotations),
    Object.keys(node_annotations)[0]
  );
  initDropdown(
    "util_link_select",
    Object.keys(link_annotations),
    Object.keys(link_annotations)[0]
  );
  updateDropDownClass("util_node_select");
  updateDropDownClass("util_link_select");
  $("#util_node_select").on("selectmenuselect", function () {
    var key = $("#util_node_select").val();
    initVariables(key, "util_node_variable", node_annotations);
  });
  $("#util_link_select").on("selectmenuselect", function () {
    var key = $("#util_link_select").val();
    initVariables(key, "util_link_variable", link_annotations);
  });
  $("#util_node_sel_btn").on("click", function () {
    selectAnnotation("node", $("#util_node_select").val(), node_annotations);
  });
  $("#util_link_sel_btn").on("click", function () {
    selectAnnotation("link", $("#util_link_select").val(), link_annotations);
  });

  $("#util_node_reset_btn").on("click", function () {
    resetSelection("util_node_reset_btn", "node");
  });
  $("#util_link_reset_btn").on("click", function () {
    resetSelection("util_link_reset_btn", "link");
  });
  setTimeout(function () {
    utilSocket.emit("getSelection");
  }, 1000);
  console.log(pdata);
  if (pdata.stateData == undefined) {
    addListener(pdata, "stateData", {});
  }
  console.log(pdata);
  if (pdata.stateData.selected == undefined) {
    addListener(pdata.stateData, "selected", null);
  }
  if (pdata.stateData.selectedLinks == undefined) {
    addListener(pdata.stateData, "selectedLinks", null);
  }
  setSelectionNumber("util_num_nodes")(pdata.stateData.selected);
  setSelectionNumber("util_num_links")(pdata.stateData.selectedLinks);
  // Node selection listener
  pdata.stateData.selectedRegisterListener(
    setSelectionNumber("util_num_nodes")
  );
  // Link selection listener
  pdata.stateData.selectedLinksRegisterListener(
    setSelectionNumber("util_num_links")
  );
});

function getSetNumberFunction(id) {
  return setSelectionNumber(id);
}
function setSelectionNumber(id) {
  return function (val) {
    if ((val == null) | (val == undefined)) {
      val = "None";
    } else {
      val = val.length;
    }
    document.getElementById(id).innerHTML = val;
  };
}
utilSocket.on("selection", function (data) {
  sessionData["selected"] = data;
});
// Turn of the Highlight button on other clients
utilSocket.on("started", function (data) {
  button = document.getElementById(data.id);
  button.value = "";
  button.disabled = true;
  $("#" + data.id).addClass("loadingButton");
});

// Turn update context depending on result
utilSocket.on("result", function (data) {
  console.log(data);
  if (data.project != sessionData["actPro"]) {
    return;
  }
  if (data.data == "annotations") {
    updatedAnnotations(data);
  } else if (data.data == "selection") {
    updateSelection(data, pdata);
  }
});
