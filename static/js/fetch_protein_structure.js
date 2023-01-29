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
    socket.emit("ex", { id: id, gif_id: gif_id, fn: "fetch" });
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
          "ProteinStructureFetch is not installed.Structure will be loaded, if you manually prepared it.";
        $("#" + message_id).css("color", "yellow");
        $("#" + message_id).text(message);
        $("#" + message_id).css("opacity", "1");
        setTimeout(function () {
          $("#" + message_id).css("opacity", "0");
        }, 5000);
        document.getElementById(gif_id).style.display = "none";
        socket.emit("ex", {
          id: id,
          opt: name,
          fn: "sel",
          message_id: message_id,
          message: message,
          gif_id: gif_id,
          color: "yellow",
        });
      },
    });
  });
}
function evaluateResults(id, data, name, message_id, gif_id) {
  var message = "";
  color = "green";
  if (data["already_exists"].includes(name)) {
    message = "Structure loaded. Turn on overwrite to reprocess it.";
  } else if (name in data["alternative_ids"]) {
    var old = name;
    name = data["alternative_ids"][name];
    message =
      "Alternative structure downloaded: " +
      name +
      "! " +
      "Updated accordingly" +
      updateUniprot(name, old);
  } else if (name in data["results"]) {
    message = "Structure downloaded!";
  } else if (data["not_fetched"].includes(name)) {
    message =
      "Could not fetch a structure with this UniProt ID from AlphaFold DB!";
    color = "red";
  }
  $("#" + message_id).css("color", "red");
  $("#" + message_id).text(message);
  $("#" + message_id).css("opacity", "1");
  document.getElementById(gif_id).style.display = "none";
  socket.emit("ex", {
    id: id,
    opt: name,
    fn: "sel",
    message_id: message_id,
    message: message,
    gif_id: gif_id,
    color: color,
  });
  setTimeout(function () {
    $("#" + message_id).css("opacity", "0");
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
