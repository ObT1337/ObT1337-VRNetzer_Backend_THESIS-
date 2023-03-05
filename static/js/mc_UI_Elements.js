// SOME FUNCTIONS TO CREATE MULTICASTED (via socketIO) UI ELEEMENTS LIKE BUTTONS, DROPDOWNS, SLIDERS, CHECKBOXES

function initDropdown(id, data, active) {
  $("#" + id).selectmenu();
  for (let i = 0; i < data.length; i++) {
    $("#" + id).append(new Option(data[i]));
  }
  $("#" + id).val(active);
  $("#" + id).selectmenu("refresh");
  $("#" + id).on("selectmenuselect", function () {
    emitSelectmenuSelect(id);
  });
}

/// a test to add json string as attribute to dropdown option
function initDropdownX(id, data, active) {
  $("#" + id).selectmenu();

  for (let i = 0; i < data.length; i++) {
    var addata = { id: i, size: 99, city: makeid(5) };

    $("<option>")
      .val("object.val")
      .text(data[i])
      .attr("data-x", JSON.stringify(addata))
      .appendTo("#" + id);
  }

  $("#" + id).val(active);
  $("#" + id).selectmenu("refresh");

  $("#" + id).on("selectmenuselect", function () {
    var name = $("#" + id)
      .find(":selected")
      .text();
    var x = $("#" + id)
      .find(":selected")
      .attr("data-x");
    socket.emit("ex", { id: id, opt: name, fn: "sel", data: x });
    console.log(JSON.parse(x));
  });
}

function initSlider(id) {
  value = document.createElement("input");
  value.setAttribute("id", id + "_val");
  value.setAttribute("type", "number");
  value.setAttribute("value", 128);
  value.setAttribute("style", "display:none");
  $("#" + id).slider({
    animate: true,
    range: "max",
    min: 0,
    max: 255,
    value: 128,
    slide: function (event, ui) {
      $("#" + id + "_val").val(ui.value);
      ue4("slider", { id: id, val: ui.value });
    },
    stop: function (event, ui) {
      socket.emit("ex", { id: id, val: ui.value, fn: "sli" });
    },
  });
}

function initCheckbox(id) {
  $("#" + id, function () {
    socket.emit("ex", { id: id, val: $("#" + id).is(":checked"), fn: "chk" });
  });
  $("#" + id).on("click", function () {
    socket.emit("ex", { id: id, val: $("#" + id).is(":checked"), fn: "chk" });
  });
}

function initButton(id) {
  $("#" + id).on("click", function () {
    var $this = $(this);
    socket.emit("ex", { id: id, val: $this.val(), fn: "but" });
  });
  if (id == "backwardstep") {
    initBackwardStep();
  } else if (id == "forwardstep") {
    initForwardStep();
  } else if (id == "reset") {
    initResetButton();
  }
}

function makeid(length) {
  var result = "";
  var characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  var charactersLength = characters.length;
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}
function deactivateTabs(id) {
  // Deactivate all tabs which are not contained in the html
  var tabs = document.getElementById(id);
  var items = tabs.getElementsByTagName("li");
  for (var i = 0; i < items.length; i++) {
    hyperlink = items[i].getElementsByTagName("a")[0];
    var id = hyperlink.href.split("#")[1];
    if (!document.getElementById(id)) {
      items[i].style.display = "none";
    } else {
      items[i].style.display = "inline";
    }
  }
}
function setHref(id, uniprot, link) {
  var href = link.replace("<toChange>", uniprot);
  console.log(href);
  $("#" + id).attr("href", href);
}
function followLink(link) {
  var url = "http://" + window.location.href.split("/")[2];
  window.location.href = url + link;
}

function initResetButton() {
  $("#reset").on("click", function () {
    ["layouts", "nodecolors", "links", "linkcolors"].forEach((id) => {
      $("#" + id).prop("selectedIndex", 0);
      $("#" + id).selectmenu("refresh");
    });
  });
}

function setStatus(status, id, message, timeout = 5000) {
  console.log(status, id, message, timeout);
  if (status == "error") {
    $("#" + id).css("color", "red");
  } else if (status == "success") {
    $("#" + id).css("color", "green");
  } else if (status == "warning") {
    $("#" + id).css("color", "yellow");
  }
  $("#" + id).text(message);
  $("#" + id).css("opacity", "1");
  setTimeout(function () {
    $("#" + id).css("opacity", "0");
  }, timeout);
}
function scrollHorizontal(id) {
  var item = document.getElementById(id);

  item.addEventListener("wheel", function (e) {
    if (e.deltaY > 0) {
      item.scrollLeft += 100;
      e.preventDefault();
      // prevenDefault() will help avoid worrisome
      // inclusion of vertical scroll
    } else {
      item.scrollLeft -= 100;
      e.preventDefault();
    }
  });
}

function refreshWithoutEmit(id, event_name = "selectmenuselect") {
  var selectMenu = $("#" + id);
  var selectmenuselectHandler = jQuery._data(selectMenu[0], "events")[
    event_name
  ][0].handler;
  selectMenu.off(event_name, selectmenuselectHandler);
  selectMenu.selectmenu("refresh");
  selectMenu.on(event_name, selectmenuselectHandler);
}

function nextLayout(id) {
  var idx = $("#" + id).prop("selectedIndex");
  var numOptions = $("#" + id).children().length;
  if (idx == numOptions - 1) {
    idx = 0;
  } else {
    idx++;
  }
  $("#" + id).prop("selectedIndex", idx);
  refreshWithoutEmit(id);
}
function prevLayout(id) {
  var idx = $("#" + id).prop("selectedIndex");
  if (idx == 0) {
    idx = -1;
  } else {
    idx--;
  }
  $("#" + id).prop("selectedIndex", idx);
  refreshWithoutEmit(id);
}
function initBackwardStep() {
  $("#backwardstep").on("click", function () {
    if (document.getElementById("chbXYZ").checked == true) {
      prevLayout("layouts");
    }
    if (document.getElementById("chbNrgb").checked == true) {
      prevLayout("nodecolors");
    }
    if (document.getElementById("chbLXYZ").checked == true) {
      prevLayout("links");
    }
    if (document.getElementById("chbLrgb").checked == true) {
      prevLayout("linkcolors");
    }
  });
}
function initForwardStep() {
  $("#forwardstep").on("click", function () {
    if (document.getElementById("chbXYZ").checked == true) {
      nextLayout("layouts");
    }
    if (document.getElementById("chbNrgb").checked == true) {
      nextLayout("nodecolors");
    }
    if (document.getElementById("chbLXYZ").checked == true) {
      nextLayout("links");
    }
    if (document.getElementById("chbLrgb").checked == true) {
      nextLayout("linkcolors");
    }
  });
}

function emitSelectmenuSelect(id) {
  var name = $("#" + id)
    .find(":selected")
    .text();
  socket.emit("ex", { id: id, opt: name, fn: "sel" });
  ///logger($('#selectMode').val());
}
