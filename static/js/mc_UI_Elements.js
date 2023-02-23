// SOME FUNCTIONS TO CREATE MULTICASTED (via socketIO) UI ELEEMENTS LIKE BUTTONS, DROPDOWNS, SLIDERS, CHECKBOXES

function initDropdown(id, data, active) {
  $("#" + id).selectmenu();
  for (let i = 0; i < data.length; i++) {
    $("#" + id).append(new Option(data[i]));
  }
  $("#" + id).val(active);
  $("#" + id).selectmenu("refresh");
  $("#" + id).on("selectmenuselect", function () {
    var name = $("#" + id)
      .find(":selected")
      .text();
    socket.emit("ex", { id: id, opt: name, fn: "sel" });
    ///logger($('#selectMode').val());
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
  $("#" + id).slider({
    animate: true,
    range: "max",
    min: 0,
    max: 255,
    value: 128,
    slide: function (event, ui) {
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
function setStateData(pdata) {
  $(document).ready(function () {
    var selections = pdata["stateData"];
    if (selections != undefined) {
      var ids = ["layouts", "nodecolors", "links", "linkcolors"];
      ids.forEach((id) => {
        if (selections[id] != undefined) {
          $("#" + id).val(selections[id]);
          setTimeout(function () {
            socket.emit("ex", { id: id, opt: selections[id], fn: "sel" });
          }, 5000);
        }
      });
      var ids = [
        "slider-node_size",
        "slider-link_size",
        "slider-link_transparency",
        "slider-label_scale",
      ];
      ids.forEach((id) => {
        if (selections[id] != undefined) {
          $("#" + id).slider("value", selections[id]);
          setTimeout(function () {
            socket.emit("ex", { id: id, val: selections[id], fn: "sli" });
          }, 5000);
        }
      });
      if (selections["main_tab"] != undefined) {
        $("#tabs").tabs("option", "active", selections["main_tab"]);
      }
    }
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
