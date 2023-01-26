function initMyStructureDropdown(id, data, active, message_id, gif_id) {
  $("#" + id).selectmenu();

  for (let i = 0; i < data.length; i++) {
    $("#" + id).append(new Option(data[i]));
  }

  $("#" + id).val(active);
  $("#" + id).selectmenu("refresh");

  $("#" + id).on("selectmenuselect", function () {
    var elem = $("#" + id).find(":selected");
    var name = elem.text();
    var base_url = "http://" + window.location.href.split("/")[2];
    var url = base_url + "/vrprot/fetch?id=" + name;
    document.getElementById(gif_id).style.display = "block";
    $.ajax({
      type: "POST",
      url: url,
      cache: false,
      contentType: false,
      processData: false,
      success: function (data) {
        evaluateResults(id, data, name, message_id, gif_id);
      },
      error: function (err) {
        console.log(err);
        message =
          "<h4 style=color:yellow;font-size:20px;>" +
          "ProteinStructureFetch is not installed.Structure will be loaded, if you manually prepared it." +
          "</h4 >";
        $("#" + message_id).html(message);
        setTimeout(function () {
          $("#" + message_id).html("");
        }, 5000);
        document.getElementById(gif_id).style.display = "none";
        socket.emit("ex", { id: id, opt: name, fn: "sel" });
      },
    });
  });
}
function evaluateResults(id, data, name, message_id, gif_id) {
  var message = "";
  if (data["already_exists"].includes(name)) {
    message =
      "<h4 style=color:green;font-size:20px>" +
      "Structure loaded. Turn on overwrite to reprocess it." +
      "</h4 > ";
  } else if (name in data["alternative_ids"]) {
    var old = name;
    name = data["alternative_ids"][name];
    message =
      "<h4 style=color:green;font-size:20px>" +
      "Alternative structure downloaded: " +
      name +
      "! " +
      "Updated accordingly" +
      "</h4 >";
    updateUniprot(name, old);
  } else if (name in data["results"]) {
    message =
      "<h4 style=color:green;font-size:20px>" +
      "Structure downloaded!" +
      " </h4 > ";
  } else if (data["not_fetched"].includes(name)) {
    message =
      "<h4 style=color:red;font-size:20px>" +
      "Could not fetch a structure with this UniProt ID from AlphaFold DB!" +
      "</h4 > ";
  }
  $("#" + message_id).html(message);
  document.getElementById(gif_id).style.display = "none";
  socket.emit("ex", { id: id, opt: name, fn: "sel" });
  setTimeout(function () {
    $("#" + message_id).html("");
  }, 10000);
}

function updateUniprot(name, old) {
  id = node_id;
  var base_url = "http://" + window.location.href.split("/")[2];
  var url =
    base_url +
    "/vrprot/update_uniprot?id=" +
    id +
    "&uniprot=" +
    name +
    "&old=" +
    old;
  $.ajax({
    type: "POST",
    url: url,
    data: JSON.stringify({ name: name }),
    contentType: "application/json",
    success: function (data) {
      // Updates the nodepanel to the new id to reflect the change
      socket.emit("ex", { id: "x", data: id, fn: "nlc" });
      socket.emit("ex", {
        msg: last_active_node_panel,
        id: "nodepanel_tabs",
        fn: "cht",
      });
      console.log(data);
    },
    error: function (err) {
      console.log(err);
    },
  });
}
