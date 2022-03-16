/////// USER EDITABLE
/////// HERE ARE BUTTON MAPPINGS FROM HTML FILE
/////// AND CALLS TO FLASK AND VRNetzer_API
// add MAPPINGS TO UI ELEMENTS HERE //

$(document).ready(function () {

    //LOAD NAMESPACE MENU TAB 1
    $(function () {
        $("#namespaces").selectmenu();

    });

    $('#namespaces').on('selectmenuselect', function () {
        var name = $('#namespaces').find(':selected').text();
        /////logger(name);
        UpdateNamespace(name);

    });

    //LOAD FILE MENU TAB 1
    $(function () {
        $("#layouts").selectmenu();
    });
    $('#layouts').css({
        'width': 50
    });

    $('#layouts').on('selectmenuselect', function () {
        var name = $('#layouts').find(':selected').text();
        /////logger(name);
        GetDbNodeList1(name, "A");
    });

    $(function () {
        $("#layoutsB").selectmenu();
    });

    $('#layoutsB').on('selectmenuselect', function () {
        var name = $('#layoutsB').find(':selected').text();
        //
        GetDbNodeList1(name, "B");
    });



	
	var morph = 0;
	
	$(function () {
        $("#canMorph").button();
        $("#canMorph").click(function (event) {
            event.preventDefault();
            // GetDbLinkList1();
            if (morph == 1) {
                $('#canMorph').html("MORPHING OFF");
				$('#channelB').hide();
                morph = 0;

            } else {
                $('#canMorph').html("MORPHING ON");
				$('#channelB').show();
                morph = 1;
            }
            
        });
    });

    var morphchannel = 1;

    $(function () {
        $("#MorphState").button();
        $("#MorphState").click(function (event) {
            event.preventDefault();
            // GetDbLinkList1();
            if (morphchannel == 1) {
                $('#MorphState').html("> B");
                morphchannel = 0;

            } else {
                $('#MorphState').html("A <");
                morphchannel = 1;
            }
            ue4("Morph", "A");
        });
    });

    $(function () {
        $("#reload").button();
        $("#reload").click(function (event) {
            event.preventDefault();
            GetDbLinkList1();

        });
    });

    var linkfadeState = 1;

    $(function () {
        $("#linkfade").button();
        $("#linkfade").click(function (event) {
            event.preventDefault();

            if (linkfadeState == 1) {
                $('#linkfade').html("OFF");
                linkfadeState = 0;

            } else {
                $('#linkfade').html("ON");
                linkfadeState = 1;

            }
            ue4("linkfade", linkfadeState);
        });
    });

    $(function () {
        $("#test").button();
        $("#test").click(function (event) {
            event.preventDefault();
            ue4("test", "oggggoggogg");
            ExportPdf();
        });
    });

    $(function () {
        $("#tabs").tabs();
    });

    //selection menu tab-2

    $(function () {
        $("#selectMode").selectmenu();
        $('#selectMode').append($('<option>', {
                value: "NEW",
                text: "NEW",
            }));
        $('#selectMode').append($('<option>', {
                value: "ADD",
                text: "ADD",
            }));
        $('#selectMode').append($('<option>', {
                value: "SUB",
                text: "SUB",
            }));
        $('#selectMode').val("NEW"); //SET ACTIVE SLOT
        $('#selectMode').hide();
        $('#selectMode').selectmenu("refresh");

    });

    $('#selectMode').on('selectmenuselect', function () {

        ///logger($('#selectMode').val());
    });

    $(function () {
        $("#selections").selectmenu();
    });

    $('#selections').on('selectmenuselect', function () {
        var name = $('#selections').find(':selected').val();
        ue4("loadSelection", "loadSelection");
        ///logger(name);
    });

    $(function () {
        $("#LoadSelection").button();
        $("#LoadSelection").click(function (event) {
            event.preventDefault();
            var name = $('#selections').find(':selected').val();
            ///logger(name);
            LoadSelectionDB(name);

        });
    });

    //var selcount = 0;

    $(function () {
        $("#saveSel").button();
        $("#saveSel").click(function (event) {
            event.preventDefault();

            ActivateVRkeyboard("saveSel");
        });
    });

    // SLIDERS for tabs-3


    $(function () {
        $("#slider_scale").slider({
            animate: true,
            range: "max",
            min: 0,
            max: 255,
            value: 128,
            slide: function (event, ui) {
                var scale = {"scale":ui.value};
                ue4("SetScale",scale);
            }
        });

        $("#slider-node_size").slider({
            animate: true,
            range: "max",
            min: 0,
            max: 255,
            value: 128,
            slide: function (event, ui) {
                var nsize = {"nsize":ui.value};
                ue4("SetNodeSize", nsize);
            }
        });

        $("#slider-link_size").slider({
            animate: true,
            range: "max",
            min: 0,
            max: 255,
            value: 128,
            slide: function (event, ui) {
                var lsize = {"lsize":ui.value};
                ue4("SetLinkSize", lsize);
            }
        });

        $("#slider-link_transparency").slider({
            animate: true,
            range: "max",
            min: 0,
            max: 255,
            value: 128,
            slide: function (event, ui) {
                var ltra = {"ltra":ui.value};
                ue4("SetLinkAlpha", ltra);
            }
        });

        $("#slider-light").slider({
            animate: true,
            range: "max",
            min: 0,
            max: 255,
            value: 128,
            slide: function (event, ui) {
                var light = {"light":ui.value};
                ue4("SetLight", light);

            }
        });
        ue4("Init", "init");
    });

    // Tabs-3




    $(function () {
        $("#left_handed").checkboxradio({
            icon: false,
        });
    });

    // SLIDERS FOR RANDOMWALK tab-6


    $(function () {
        $("#slider-restart_probability").slider({
            animate: true,
            range: "max",
            min: 1,
            max: 100,
            value: 20,
            slide: function (event, ui) {
                var restartLabel = "RESTART PROBABILITY: " + $("#slider-restart_probability").slider("value") / 100;
                $("#restart_probability").html(restartLabel);
            }
        });
        // var restartLabel = "RESTART PROBABILITY: " + $("#slider-restart_probability").slider("value")
        $("#restart_probability").val($("#slider-restart_probability").slider("value"));
    });

    // TAB4 SEARCH
    $(function () {
        $("#searchAttribute1").selectmenu();
        $('#searchAttribute1').append($('<option>', {
                value: "NODE",
                text: "NODE",
            }));
        $('#searchAttribute1').append($('<option>', {
                value: "DISEASE",
                text: "DISEASE",
            }));
        $('#searchAttribute1').append($('<option>', {
                value: "PATHWAY",
                text: "PATHWAY",
            }));
        $('#searchAttribute1').append($('<option>', {
                value: "molecular_function",
                text: "molecular_function",
            }));
        $('#searchAttribute1').append($('<option>', {
                value: "cellular_component",
                text: "cellular_component",
            }));
        $('#searchAttribute1').append($('<option>', {
                value: "biological_process",
                text: "biological_process",
            }));
        $('#searchAttribute1').append($('<option>', {
                value: "TISSUE",
                text: "TISSUE",
            }));
        $('#searchAttribute1').append($('<option>', {
                value: "HUMAN_PHENOTYPE",
                text: "HUMAN_PHENOTYPE",
            }));
        $('#searchAttribute1').append($('<option>', {
                value: "OMIM_DISEASE",
                text: "OMIM_DISEASE",
            }));
        $('#searchAttribute1').val("TISSUE"); //SET ACTIVE SLOT
        $("#searchAttribute1").selectmenu("refresh");
    });

    $('#searchAttribute1').on('selectmenuselect', function () {
        var name = $('#searchAttribute1').find(':selected').text();
        //if in mode search node, hide button row above
        if (name == "NODE") {
            ///logger("nodes selected");
            $('#searchGroup1').hide("drop", {
                direction: "down"
            }, "fast");
        } else {
            $('#searchGroup1').show("fold", 100);
        }
        /////logger("Attribute says: "+ name);
    });

    $(function () {
        $("#searchInput1").button();
        $("#searchInput1").attr("searchID", -1);
        $("#searchInput1").click(function (event) {
            event.preventDefault();
            ActivateVRkeyboard("searchInput1");

            //GetDbSearchTerms("af", $('#searchAttribute1').val());

        });
    });

    //desktop version input field1
    $("#search_txt").keyup(function () {
        GetDbSearchTerms($(this).val(), $('#searchAttribute1').val());
    });

    $(function () {
        $("#searchMode1").selectmenu();
        $('#searchMode1').append($('<option>', {
                value: "NEW",
                text: "NEW",
            }));
        $('#searchMode1').append($('<option>', {
                value: "ADD",
                text: "ADD",
            }));
        $('#searchMode1').append($('<option>', {
                value: "SUB",
                text: "SUB",
            }));
        $('#searchMode1').val("NEW"); //SET ACTIVE SLOT
        $('#searchMode1').hide();
        $('#searchMode1').selectmenu("refresh");

    });

    $(function () {
        $("#searchGO").button();
        $("#searchGO").click(function (event) {
            event.preventDefault();
            var id = $("#searchInput1").attr("searchID");

            SimpleSearch(id);
        });
    });



    //buttons fuer randomwalk

    $(function () {
        $("#start_randomwalk_button").button();
        $("#start_randomwalk_button").click(function (event) {
            event.preventDefault();
            //var span_Text = document.getElementById("restart_probability").innerText;
            var restartpr = $("#slider-restart_probability").slider("value") / 100;
            ///logger(restartpr)
            ue4("StartRandomWalk", restartpr);

            //reloadForceLayout (inputdata1);
        });
    });

    $(function () {
        $("#clear_randomwalk_button").button();
        $("#clear_randomwalk_button").click(function (event) {
            event.preventDefault();
            ue4("ClearRandomWalk", "bla");
            clearForceLayout(inputdata);
        });
    });

    $(function () {
        $("#start_shortestPath").button();
        $("#start_shortestPath").click(function (event) {
            event.preventDefault();
            shortestPath();
            //ue4('shortestPathTrigger','start');
            ///logger("shortest Path clicked");
        });
    });
    
    $(function () {
        $("#clear_shortestPath").button();
        $("#clear_shortestPath").click(function (event) {
            event.preventDefault();
            $('#spLabel').empty();
            ue4('shortestPathClear','start');
            ///logger("shortest Path clicked");
        });
    });

    $(function () {
        $("#p1_shortestPath").button();
        $("#p1_shortestPath").click(function (event) {
            event.preventDefault();
            ue4('shortestPathPoint', 'p1');
            /////logger("shortest Path clicked");
        });
    });

    $(function () {
        $("#p2_shortestPath").button();
        $("#p2_shortestPath").click(function (event) {
            event.preventDefault();
            ue4('shortestPathPoint', 'p2');
            /////logger("shortest Path clicked");
        });
    });

    $(function () {
        $("#reLayout").button();
        $("#reLayout").click(function (event) {
            event.preventDefault();

            var out = {
                "content": "doesntmatter",
                "route": "reLayout"
            };
            ue4("GetSelection", out);
            

        });
    });

    //start_GSEA

    $(function () {
        $("#GSEAAttributes").selectmenu();
        $('#GSEAAttributes').append($('<option>', {
                value: "ALL",
                text: "ALL",
            }));
        $('#GSEAAttributes').append($('<option>', {
                value: "DISEASE",
                text: "DISEASE",
            }));
        $('#GSEAAttributes').append($('<option>', {
                value: "PATHWAY",
                text: "PATHWAY",
            }));
        $('#GSEAAttributes').append($('<option>', {
                value: "molecular_function",
                text: "molecular_function",
            }));
        $('#GSEAAttributes').append($('<option>', {
                value: "cellular_component",
                text: "cellular_component",
            }));
        $('#GSEAAttributes').append($('<option>', {
                value: "biological_process",
                text: "biological_process",
            }));
        $('#GSEAAttributes').append($('<option>', {
                value: "TISSUE",
                text: "TISSUE",
            }));
        $('#GSEAAttributes').append($('<option>', {
                value: "HUMAN_PHENOTYPE",
                text: "HUMAN_PHENOTYPE",
            }));
        $('#GSEAAttributes').append($('<option>', {
                value: "OMIM_DISEASE",
                text: "OMIM_DISEASE",
            }));
        $('#GSEAAttributes').val("ALL"); //SET ACTIVE SLOT
        $("#GSEAAttributes").selectmenu("refresh");
    });

    $('#GSEAAttributes').on('selectmenuselect', function () {
     
    });


    $(function () {
        $("#start_GSEA").button();
        $("#start_GSEA").click(function (event) {
            event.preventDefault();
            
            var name = $('#GSEAAttributes').find(':selected').text();

            var out = {
                "content": name,
                "route": "GSEA"
            };
            ue4("GetSelection", out);
            
        });
    });


    $(function () {
        $("#exitIsolate").button();
        $("#exitIsolate").click(function (event) {
            event.preventDefault();
            //var out = {"content":"doesntmatter", "route":"reLayout"};
            ue4("exitIsolate", "exitIsolateSelection");

        });
    });

    $(function () {
        $("#nextslide").button();
        $("#nextslide").click(function (event) {
            event.preventDefault();
            pp_count++;
            var path = "/static/img/powerpoint/Slide" + pp_count + ".jpg";

            document.getElementById("powerpoint").src = path;
            /*         var img = document.createElement("IMG");
            img.src = "img/powerpoint/Slide1.jpg";
            var oldImg = document.getElementById('powerpoint');
            document.getElementById('powerpoint').replaceChild(img, oldImg); */
        });
    });

    $(function () {
        $("#RefreshProjects").button();
        $("#RefreshProjects").click(function (event) {
            event.preventDefault();
            GetDbFileNames1();
        });
    });
    
    
    ///////INIT HERE
    $("#spinner").hide();
    $("#spinner_load").hide();
    $('#channelB').hide();
    GetDbFileNames1();

    //var buttons = document.getElementById("pphenobox").children;

    // INITIALIZE STUFF HERE
    //read files and populate ui's


    /*     document.getElementById("SendButton").onclick = function() {
    postFlask("/_receive_json/", nodes)
    };
    document.getElementById("ReadButton").onclick = function() {
    postFlask("/_request_json/", requestTxt)
    }; */

    /*     $( "#slider-6" ).slider({
    range:false,
    min: 0,
    max: 500,
    values: [250],

    slide: function( event, ui ) {
    // $( "#slidevalue" )
    //.val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
    ///logger(ui.values[ 0 ] );
    ue4("print", ui.values[ 0 ]);
    }
    }); */

});