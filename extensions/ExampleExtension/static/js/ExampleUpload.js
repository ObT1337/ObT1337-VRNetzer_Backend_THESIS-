$(document).ready(function() {
    document.getElementById("example_new_namespace_name").readOnly = true;
    $(function () {
      $("#example_upload_namespaces").selectmenu({
        classes:{
            "ui-selectmenu-open": "twozerozero-open",
        },
      });
    });
    $('#example_upload_namespaces').on('selectmenuselect', function () {
      var name = $('#example_upload_namespaces').find(':selected').text();
      console.log(name);
  
    });
  
    $("#example_upload_button").button();
    $("input:radio[name='example_namespace']").change(function () {
      if ($(this).val() == "New") {
        document.getElementById("example_new_namespace_name").readOnly = false;
        $("#example_upload_namespaces").selectmenu("disable");
      } else {
        document.getElementById("example_new_namespace_name").readOnly = true;
        $("#example_upload_namespaces").selectmenu("enable");
      }
      console.log("37: New namespace:" + $("#new_namespace_name").val());
    });
    $("#example_new_namespace_name").on("click", function() {
      this.readOnly = false;
      $("#example_upload_namespaces").selectmenu("disable");
      document.getElementById("example_radio_new_namespace").checked = true;
    });
    $("#example_framebox_exisiting").on("click", function() {
      $("#example_new_namespace_name").readOnly = true;
      $("#example_upload_namespaces").selectmenu("enable");
      document.getElementById("example_radio_existing").checked = true;
    });
    $("#example_upload_form").on("change input", function () {
      console.log("changed!");
      var example_formData = new FormData(document.getElementById("example_upload_form"));
      for (var pair of example_formData.entries()) {
        console.log("47: pairs: " + pair[0] + ", " + pair[1]);
      }
    });
  
    $("#example_upload_form").submit(function(event) {
      console.log("Submitting")
  
      $("#example_upload_message").html("Uploading...");
      // document.getElementById("upload_button").style.backgroundImage = "{{ url_for('static', filename = 'img/active_gears.png') }}";
      document.getElementById("example_upload_button").value = '...';
      document.getElementById("example_upload_button").disabled = true;
  
      event.preventDefault();
  
      var form = $(this);
      var formData = new FormData(this);
      if (formData.get("example_namespace") == "existing") {
        formData.append("existing_namespace", $("#example_upload_namespaces").val());
      }
      let it = formData.keys();
  
      let result = it.next();
      while (!result.done) {
        console.log("101: Result: " + result); // 1 3 5 7 9
        console.log("102: Result_value:" + formData.get(result.value));
        result = it.next();
        };
      var base_url = "http://" + window.location.href.split("/")[2]; // Not sure why no todo it like this. Maybe if the server runs on a different ip than the uploader?
      var url = base_url + "/ExampleExtension/uploadfiles";
      console.log("107: URL:", url);
      console.log("108: FormData:", formData);
      $.ajax({
        type: "POST",
        url: url,
        data: formData, // serializes the form's elements.
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
          console.log("117: Data: " + data);
          $("#example_upload_message").html("Upload successful: " + data);
          document.getElementById("example_upload_button").value = "Upload"; 
          document.getElementById("example_upload_button").disabled = false;
        },
        error: function (err) {
          console.log("Uploaded failed!");
          $("#example_upload_message").html("Upload failed!");
          document.getElementById("example_upload_button").value = "Upload"; 
          document.getElementById("example_upload_button").disabled = false;
        },
      });
    });
  });
  