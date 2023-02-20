function getSelections() {
  message = {
    layout: $("#layouts").val(),
    nodecolors: $("#nodecolors").val(),
    links: $("#links").val(),
    linkcolors: $("#linkcolors").val(),
    main_tab: $("#tabs").tabs("option", "active"),
  };
  return message;
}

function updateSelection(data) {
  if (data.type == "node") {
    pdata.stateData.selected = data.selection;
  } else if (data.type == "link") {
    pdata.stateData.selectedLinks = data.selection;
  }
  console.log(pdata);
}

function updatedAnnotations(data) {
  if (data.type == "node") {
    node_annotations = {};
    var keys = Object.keys(data.annotations);
    for (var i = 0; i < keys.length; i++) {
      var option = keys[i];
      var key = clearOptions(option, "node");
      node_annotations[key] = data.annotations[option];
    }
    console.log("node", node_annotations);
    updateDropDown(
      "util_node_annot",
      "util_node_select",
      "util_node_variable",
      node_annotations
    );
    updateDropDownClass("util_node_select");
  } else if (data.type == "link") {
    link_annotations = {};
    var keys = Object.keys(data.annotations);
    for (var i = 0; i < keys.length; i++) {
      var option = keys[i];
      var key = clearOptions(option, "link");
      link_annotations[key] = data.annotations[option];
    }
    console.log("link", link_annotations);
    updateDropDown(
      "util_link_annot",
      "util_link_select",
      "util_link_variable",
      link_annotations
    );
    updateDropDownClass("util_link_select");
  }
}
function selectAnnotation(type, key, annotations) {
  console.log(key);
  var data = annotations[key];
  var dtype = data.dtype;
  if ((dtype == "float") | (dtype == "int")) {
    var value = $("#util_" + type + "_int").slider("option", "value");
  } else if (dtype == "str") {
    var value = $("#util_" + type + "_str").val();
  } else if (dtype == "bool") {
    var value = $("#util_" + type + "_bool").val();
  }

  var key = clearOptions(key, type, true);
  var message = {
    dtype: dtype,
    value: value,
    annotation: key,
    type: type,
  };
  utilSocket.emit("select", message);
}
// Update selectmenu size
function updateDropDownClass(id) {
  $("#" + id).selectmenu({
    classes: {
      "ui-selectmenu-open": "limited-selectmenu-open",
    },
  });
  if (user_agent.includes("UnrealEngine")) {
    updateVRDropDownClass(id);
  }
}
// Update selectmenu font
function updateVRDropDownClass(id) {
  $("#" + id)
    .selectmenu("menuWidget")
    .menu({
      classes: {
        "ui-menu-item-wrapper": "limited-selectmenu-open-text",
      },
    });
}
// Update selectmenu options
function updateDropDown(parent, id, variable_id, annotation) {
  var options = Object.keys(annotation);
  if (options.length == 0) {
    document.getElementById(parent).style.visibility = "hidden";
    return;
  }
  document.getElementById(parent).style.visibility = "visible";
  var selectMenu = $("#" + id);
  // clear the current options
  selectMenu.empty();
  // define the list of options
  // append new options to the selectmenu
  $.each(options, function (index, option) {
    selectMenu.append($("#" + id).append(new Option(option)));
  });
  var key = $("#" + id).val();
  initVariables(key, variable_id, annotation);
  // refresh the selectmenu to update its style
  selectMenu.selectmenu("refresh");
}
function initVariables(key, variable_id, annotation) {
  var data = annotation[key];
  console.log(data);
  var dtype = data.dtype;
  var special = false;
  if (["Source Node", "Sink Node", "Name"].includes(key)) {
    special = true;
  }
  var space = document.getElementById(variable_id);

  var type = "node";
  if (variable_id.includes("link")) {
    type = "link";
  }

  if ((dtype == "float") | (dtype == "int")) {
    var max = data.max;
    var min = data.min;
    if (min >= 0) {
      min = 0;
    }
    var middle = (max + min) / 2;
    var step = 1;
    if (dtype == "float") {
      step = 0.001;
      max = Number(max.toFixed(2));
      min = Number(min.toFixed(2));
      middle = Number(middle.toFixed(2));
      if (max < 1) {
        max = 1;
      }
    } else {
      max = Math.round(max);
      min = Math.round(min);
      middle = Math.round(middle);
    }

    slider_div = document.createElement("div");
    slider_div.style = "display: flex;align-items: center;";
    element = document.createElement("div");
    element.id = "util_" + type + "_int";
    element.style = "width: 60%;";

    value = document.createElement("p");
    value.id = "util_" + type + "_int_value";
    value.style =
      "margin-left:15%;white-space: nowrap;overflow: hidden;width:25%";
    slider_div.appendChild(element);

    if (special) {
      value.innerHTML = data.values[middle];
    } else {
      value.innerHTML = middle;
    }
    slider_div.appendChild(value);
    space.innerHTML = "<p></p>";
    space.appendChild(slider_div);
    $("#util_" + type + "_int").slider({
      animate: true,
      range: "max",
      min: min,
      max: max,
      value: middle,
      step: step,
      slide: function (event, ui) {
        socket.emit("ex", {
          id: "util_" + type + "_int",
          val: ui.value,
          fn: "sli",
        });
        console.log(special);
        if (special) {
          $("#util_" + type + "_int_value").text(data.values[ui.value]);
        } else {
          $("#util_" + type + "_int_value").text(ui.value);
        }
      },
    });
  } else if (dtype == "str") {
    var options = data.options;
    element = document.createElement("select");
    element.id = "util_" + type + "_str";
    space.innerHTML = "<p></p>";
    space.appendChild(element);
    console.log(options);
    initDropdown("util_" + type + "_str", options, options[0]);
    updateDropDownClass("util_" + type + "_str");
  }
}

function clearOptions(option, type, reverse = false) {
  var replaceMap = {
    s: "Source Node",
    e: "Sink Node",
    n: "Name",
    id: type.charAt(0).toUpperCase() + type.slice(1) + " Identifier",
  };
  var to_check = Object.keys(replaceMap);
  if (reverse) {
    var tmp = replaceMap;
    replaceMap = {};
    for (var key in tmp) {
      replaceMap[tmp[key]] = key;
    }
    to_check = Object.keys(replaceMap);
  }
  if (to_check.includes(option)) {
    option = replaceMap[option];
  }
  return option;
}
