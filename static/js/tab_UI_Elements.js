// ############################################################
// extension to static/js/mc_UI_Elements.json for specific tabs
// ############################################################

function initButtonFunction(id, fun){
    $('#'+ id).on("click", function(){
      var $this = $(this);
      // socket.emit('ex', {id: id, val: $this.val(), fn: "but"});
      fun(); 
    });
}

function initDropdownFunction(id, data, placeholderVal=undefined, fun){

  $('#'+ id).selectmenu();
  // remove old options without placeholder
  $("#" + id + " option").each(function(){
    if ($(this).val() !== placeholderVal){
      $(this).remove();
    }
  })

  // set new options
  for (let i = 0; i < data.length; i++) {
    $('#'+ id).append(new Option(data[i]));
  }
  $('#'+ id).selectmenu("refresh");

  $('#'+ id).on('selectmenuselect', function () {
    fun();
  });
}
