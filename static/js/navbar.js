function initNavDropdown(id) {
    $("#"+id).selectmenu({
        classes: {
            "ui-selectmenu-button-closed": "navbar-dropdown-menu-button-closed",
            "ui-selectmenu-button-open": "navbar-dropdown-menu-button-open",
            "ui-selectmenu-text": "navbar-dropdown-text",
        },
        icons: {
            button: "navbar-triangle"
        }
    });
  
    $('#' + id).on('selectmenuselect', function() {
        window.location = $("#"+id).val();
    });
};