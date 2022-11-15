function initNavDropdown(id) {
    $("#"+id).selectmenu({
        classes: {
            "ui-selectmenu-button": "navbar-dropdown-menu",
            "ui-selectmenu-button-closed": "navbar-dropdown-menu-button-closed",
            "ui-selectmenu-button-open": "navbar-dropdown-menu-button-open",
            "ui-selectmenu-text": "navbar-dropdown-text"
        }
    });
  
    $('#' + id).on('selectmenuselect', function() {
        window.location = $("#"+id).val();
    });
};
function addToNavDropdown(category, link) {
    var dropdown = document.getElementById(category);
    var name = link[1];
    var hyperlink = link[0];
    dropdown.innerHTML += (
        '<option value="' + hyperlink + '">' + name + '</option>'
    )
};
function getAllLinks() {
    const request = async () => {
        const response = await fetch('/get_all_links');
        const json = await response.json();
        console.log(json);
    }
    
    request();
}

function setNavBarLinks(links) {
    for (var i = 0; i < links.length; i++) {
        var link = links[i];
        if (!([, "nodeinfo", "get_structure_scale", "test44", "force", "loadAllProjectsR"].includes(link[1]))) {
            if (links[1].includes("home"))
                addToNavDropdown("home_dropdown", link);
            else if (link[1].includes("main"))
                addToNavDropdown("mainpanel_dropdown", link);
            else if ((link[1].includes("nodepanel")))
                addToNavDropdown("nodepanel_dropdown", link);
            else if ((link[1].includes("upload")) & !(link[1].includes("files")))
                addToNavDropdown("uploader_dropdown", link);
            else if ((link[1].includes("preview")))
                addToNavDropdown("preview_dropdown", link);
        };
        };
};
function setHomeLinks(links) {
    for (var i = 0; i < links.length; i++) {
        var link = links[i];
        if (!(["home", "nodeinfo", "get_structure_scale", "test44", "force", "loadAllProjectsR"].includes(link[1]))) {
            if (link[1].includes("main")) {
                setLinks("mainpanels", link);
            } else if ((link[1].includes("nodepanel"))) {
                setLinks("nodepanels", link);
            } else if ((link[1].includes("upload")) & !(link[1].includes("files"))) {
                setLinks("uploader", link);
            } else if ((link[1].includes("preview"))) {
                setLinks("previews", link);
            } else {
                document.write(link[1]);
            }
        };
    };
}

function setLinks(panel, link) {
    var frameBox = document.getElementById(panel);
    var name = link[1];
    var hyperlink = link[0];
    frameBox.innerHTML += (
        '<a id='
        + name
        + ' class=crosslinks href="'
        + hyperlink
        + '">'
        + name
        + '</a>'
        + '<br>'
    )
};