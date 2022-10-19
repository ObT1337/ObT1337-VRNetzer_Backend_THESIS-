function selectEvidenceWebGL(id, opt) {
    $('#' + id).on("click", function() {
        var links = document.getElementById("linksRGB");
        console.log(pdata);
        for (let i = 0; i < links.length; i++) {
            if (links[i].text == opt) {
                console.log("selected layout:" + links[i].text);
                document.getElementById("linksRGB").selectedIndex = i;
                console.log("index:"+$('#linksRGB option:selected').index())
                // socket.emit('ex', { id: id, opt: pdata["name"], fn: "sel" });
                var url = window.location.href.split('&')[0] + '&project=' + pdata["name"] + '&layout=' + $('#layouts option:selected').index() + '&ncol=' + $('#layoutsRGB option:selected').index() + '&lcol=' + $('#linksRGB option:selected').index();
                window.location.href = url;
                break;
            }
        }
    });
}
function selectEvidenceVRNetzer(id, opt) {
    $('#' + id).on("click", function() {
        socket.emit('ex', { id: "projects", opt: opt, fn: "sel" });
    });
}