// ############################################################
// extension to static/js/mc_UI_Elements.json for specific tabs
// ############################################################

function initButtonFunction (id, fun){
    $('#'+ id).on("click", function(){
      var $this = $(this);
      // socket.emit('ex', {id: id, val: $this.val(), fn: "but"});
      fun(); 
    });
}


