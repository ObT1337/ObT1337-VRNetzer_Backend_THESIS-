///////GLOBAL VARS vvvvvvv

var p1 = -1;
var p2 = -1;
 

//create the global ue4(...) helper function
"object" != typeof ue || "object" != typeof ue.interface ? ("object" != typeof ue && (ue = {}), ue.interface = {}, ue.interface.broadcast = function (e, t) {
    if ("string" == typeof e) {
        var o = [e, ""];
        void 0 !== t && (o[1] = t);
        var n = encodeURIComponent(JSON.stringify(o));
        "object" == typeof history && "function" == typeof history.pushState ? (history.pushState({}, "", "#" + n), history.pushState({}, "", "#" + encodeURIComponent("[]"))) : (document.location.hash = n, document.location.hash = encodeURIComponent("[]"))
    }
}) : function (e) {
    ue.interface = {},
    ue.interface.broadcast = function (t, o) {
        "string" == typeof t && (void 0 !== o ? e.broadcast(t, JSON.stringify(o)) : e.broadcast(t, ""))
    }
}
(ue.interface), (ue4 = ue.interface.broadcast);
////  API DEFENITION
//// DONT TOUCH THIS FILE
function logger(message) {
    console.log(message);
    ue4("log", message);
}

//// FUNCTIONS CALLED BY UE4


ue.interface.getSelection = function (data) {
    

    switch (data.route) {
        case "saveSelection":
            /////logger(data);
            SaveSelectionDB(data);
            break;
        case "reLayout":
            ReLayoutSubSet(data);
            break;
        case "GSEA":
            GSEASubSet(data);
            break;
 

    }
  

};


ue.interface.getRandomWalkResult = function (data) {
     
    logger(data); 
    // ///logger(data.nodes[0].frequency + " id:" + data.nodes[0].id );
     
 
    reloadForceLayout(data);  // this guy somhow modifies input json???
    drawBarChart(data.nodes);
    dashboardData.rw.links = data.links;
    dashboardData.rw.nodes = data.nodes;
     
};

ue.interface.updateSeeds = function (data) {
    //  ///logger(data);
    //  ///logger("SEEDS");

    for (var i = 0; i < 100 && i < data.seeds.length; i++) {

        createButton(data.seeds[i].name, data.seeds[i].id, "seedbox");

    }

};

ue.interface.addMyGene = function (data) {
    // ///logger(data);
    // ///logger("ADD MY GENE");


    createButton(data.name, data.id, "MyNodesbox");

};

ue.interface.randomWalkPy = function (data) {
    $('#rwsection').hide("drop", {
        direction: "down"
    }, "fast");
    $('#spinner').show();
    $('#rwLabel').text("...");
    var xxx = $('#slider-restart_probability').val();

    var numSeeds = data.node_ids.length;
    data.variants = [];
    payload = JSON.stringify(data);
    ///logger(numSeeds);

    ///logger(payload);

    path = dbprefix + "/api/" + thisNamespace.namespace + "/node/random_walk";
    $.ajax({
        type: "POST",
        url: path,
        contentType: "application/json",
        data: payload,
        dataType: "json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        success: function (response) {

            response.numSeeds = numSeeds;
            ue4("rw_result", response);
            $('#rwsection').show("drop", {
                direction: "down"
            }, "fast");
            $('#spinner').hide();
            logger(response);
            $('#rwLabel').text(response.nodes.length + " NODES FOUND");
            ///logger(response);
        },
        error: function (err) {
            ///logger(err);
            $('#rwsection').show("drop", {
                direction: "down"
            }, "fast");
            $('#spinner').hide();
            $('#rwLabel').text("RANDOMWALK - ERROR");

        }
    });

};

///////////SHORTEST PATH

ue.interface.shortestPathPoint = function (data) {

    jdata = JSON.parse(data);

    ///logger(jdata.id + " " + jdata.target + " " + jdata.name);

    if (jdata.target == "p1") {
        $('#p1_shortestPath').text(jdata.name);
        p1 = jdata.id;
    } else {
        $('#p2_shortestPath').text(jdata.name);
        p2 = jdata.id;

    }
}

///UPDATE NODEPANEL

ue.interface.updateNodePanel = function (data) {

    //payload = JSON.stringify(data);
    nodePanelRequest(data.id);
    publicationsRequest(data.id);

};


function nodePanelRequest(data){
    
    path = dbprefix + "/api/" + thisNamespace.namespace + "/node/gene_card?node_id=" + data;
    logger(path);
    $.ajax({
        type: "GET",
        url: path,
        contentType: "application/json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        dataType: "json",
        success: function (response) {

            $("#iSym").text(response[0].symbol);
            $("#iName").text(response[0].name);
            $("#iDeg").text(response[0].degree + " Neighbors");

            var dtext = "DISEASES: ";
            for (var i = 0; i < 100 && i < response[0].diseases.length; i++) {
                dtext = dtext + response[0].diseases[i] + "\n";
            }
            $("#idisbox").text(dtext);

            var ftext = "FUNCTIONS: ";
            for (var i = 0; i < 100 && i < response[0].functions.length; i++) {
                ftext = ftext + response[0].functions[i] + "\n";
            }
            $("#ifunbox").text(ftext);

            ///logger(response[0].tissue);
		    // if (thisNamespace.namespace == "ppi") {
		    //     drawNodeBarChart(response[0].tissue);
		    // }
            drawNodeBarChart(response[0].tissue);

            ///logger(response);
        },
        error: function (err) {
            ///logger(err);

        }
    });
}

function publicationsRequest(data){
    
    path = dbprefix + "/api/" + thisNamespace.namespace + "/article?node_id=" + data;
    
    $.ajax({
        type: "GET",
        url: path,
        contentType: "application/json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        dataType: "json",
        success: function (response) {

            //logger(response);
            clearButtons("pubbox");
            
            //
            for (var i = 0; i < 100 && i < response.length; i++) {
                logger(response[i].title);
                createPubButton(response[i].title, response[i].external_id, "pubbox");
        
            }
            

        },
        error: function (err) {
            logger(err);

        }
    });
}

function publicationsAbstractRequest(data){
    
    path = dbprefix + "/api/" + thisNamespace.namespace + "/article?pubid=" + data;
    
    $.ajax({
        type: "GET",
        url: path,
        contentType: "application/json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        dataType: "json",
        success: function (response) {
            $("#pubdate").text(response.publication_date);
            $("#abstitle").text(response.title);
            $("#abstext").text(response.abstract);
            $("#authtext").text(response.authors_list);
            
            logger(response);
            

        },
        error: function (err) {
            logger(err);

        }
    });
}

var pp_count = 0;

ue.interface.powerpoint = function (data) {
    /////logger(data);
    jdata = JSON.parse(data);
    ///logger(data.i);
    if (pp_count > 0) {
        pp_count = pp_count + jdata.i;
        var path = "/static/img/powerpoint/Slide" + pp_count + ".jpg";

        document.getElementById("powerpoint").src = path;
    }
    // i
    //dummydata = '{"node_ids":[12149,108],"selection_name":"somAARGrgARGagname"}';
    //input = JSON.parse(data);
    /////logger(input);


};

ue.interface.addPhen = function (data) {
    ///logger(data.nodes[0]);
    createButton(data.nodes[0].name, data.nodes[0].id, "pphenobox");

};

function juliaRw(data) {

    $('#prw_section').hide("drop", {
        direction: "down"
    }, "fast");
    $('#pspinner_load').show();
    //$('#rwLabel').text("...");


    var numSeeds = data.node_ids.length;
    //data.variants = [13991,2313,7036,16851,17944,5766];
    payload = JSON.stringify(data);
    /////logger(numSeeds);

    /////logger(payload);

    path = dbprefix + "/api/ppi/node/random_walk_dock2";
    /////logger(path);

    $.ajax({
        type: "POST",
        url: path,
        contentType: "application/json",
        data: payload,
        dataType: "json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        success: function (response) {
          
            response.numSeeds = numSeeds;
            dashboardData.rw.links = response.links;
            dashboardData.rw.nodes = response.nodes;
            // ue4("rw_result",response);
            $('#prw_section').show("drop", {
                direction: "down"
            }, "fast");
            $('#pspinner_load').hide();
            /////logger(response);
            //$('#rwLabel').text(response.length + " NODES FOUND");
            logger(response);
            logger("this");
 
            reloadForceLayout(response);
            /////logger(response.nodes[0].symbol);
            var clippedNodes = [];
            var nodesJson = {
                "seeds": [],
                "variants": [],
                "linker": [],
                "mode": "NEW"
            };

            for (var i = 0; i < response.nodes.length; i++) {
                /////logger(response.nodes[i].group);
                var thisnode = {
                    "node_id": response.nodes[i].id
                };

                if (response.nodes[i].group == 2) {
                    nodesJson.variants.push(thisnode);
                    clippedNodes.push(response.nodes[i]);
                } else if (response.nodes[i].group == 0) {
                    nodesJson.seeds.push(thisnode);
                } else if (response.nodes[i].group == 1) {
                    nodesJson.linker.push(thisnode);
                }
            }
            ///logger(nodesJson);
            drawBarChart(clippedNodes);


            ue4("julia", nodesJson);

        },
        error: function (err) {
            ///logger(err);
            /*         $('#rwsection').show( "drop", { direction: "down" }, "fast" );
            $('#spinner').hide();
            $('#rwLabel').text("RANDOMWALK - ERROR"); */

        }
    });

}

function shortestPath() {

    path = dbprefix + "/api/" + thisNamespace.namespace + "/node/shortest_path?from=" + p1 + "&to=" + p2;
    ///logger(path);
    $('#ShortestPathSection').hide("drop", {
        direction: "down"
    }, "fast");
    $('#spinner').show();
    //$('#spLabel').text("...");
    $.ajax({
        type: "GET",
        url: path,
        contentType: "application/json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        dataType: "json",
        success: function (response) {
            /////logger(response);
            $('#spLabel').empty();
            ue4("shortestPathResponse", response);
            for (var i = 0; i < response.nodes.length; i++) {
                createButton(response.nodes[i].symbol, response.nodes[i].node_id, "spLabel");
            }

            /////logger(response);
            $('#spinner').hide("drop", {
                direction: "down"
            }, "fast");
            $('#ShortestPathSection').show();
            //$('#spLabel').text(response);


        },

        error: function (err) {
            ///logger(err);

            $('#ShortestPathSection').show("drop", {
                direction: "down"
            }, "fast");
            $('#spinner').hide();
            $('#spLabel').text("ERROR");

        }
    });

};

// call a function named route + "Trigger" defined below for each input field
ue.interface.VRkeyboard = function (payload) {
    input = JSON.parse(payload);
    // Call function dynamically
    var fnName = input.route + "Trigger"; ;
    window[fnName](input);
    ///logger("VRKeyboard triggered:" + fnName);
};

// TEXT INPUT FIELDS
function searchInput1Trigger(data) {
    /////logger(data);
    // SET BUTTON TEXT
    var element = "#" + data.route;
    $(element).html(data.content);
    /////logger(data.content);
    GetDbSearchTerms(data.content, $('#searchAttribute1').val());

    /*     if (data.end == 1){
    ///logger(data.route + " Event Fired");
    } */
}

function SaveSearchTrigger(data) {
    ///logger(data);
    // SET BUTTON TEXT
    //var element = "#" + data.route;
    //$(element).html(data.content);
    data.route = "saveSelection";

    if (data.end == 1) {
        ue4("getSelection", data.content);
        ///logger(data.route + " Event Fired");
    }
}

function saveSelTrigger(data) {
    data.route = "saveSelection";
    ///logger(data);
    if (data.end == 1) { //USER PRESSED ENTER KEY
        // Get Selection from UE4 somehow
        ue4("getSelection", data);
    }
}

function saveResultsTrigger(data) {
    data.route = "saveResults";

    if (data.end == 1) { //USER PRESSED ENTER KEY
        //todo: gather panel data
        CollectDashBoardData();
        dashboardData.filename = data.content;
        SavePanelData(dashboardData);
        
    }
}

ue.interface.setFilenames = function (payload) {
    input = JSON.parse(payload);
    /////logger("setFilenames says:");
    /////logger(input.nodes[1]);

    // POPULATE UI DROPDOWN
    input.nodes.forEach(function (item) {
        $('#selections').append($('<option>', {
                value: 1,
                text: item
            }));

        $('#pselections').append($('<option>', {
                value: 1,
                text: item
            }));

    });

};

var dbdata;
var thisNamespace;

ue.interface.setNamespace = function (data) {
    //input = JSON.parse(data);
    
    thisNamespace = data;
    logger(thisNamespace);

};
//// Functions that POST to UE4 //////

function ActivateVRkeyboard(route) {
    ue4("VRkeyboard", route);
    ///logger("vrkeyboard");
}

////put functions that POST to Flask HERE vvv
function UpdateNamespace(name) {

    thisNamespace = dbdata.find(o => o.namespace === name);
    
    logger(thisNamespace);
    ///notify ue4
    ue4("namespace", thisNamespace);
    //CLEAR LAYOUT DROPDOWN
    $('#layouts').find('option').remove().end();
    $('#layouts').selectmenu('destroy').selectmenu({
        style: 'dropdown'
    });
    $('#layoutsB').find('option').remove().end();
    $('#layoutsB').selectmenu('destroy').selectmenu({
        style: 'dropdown'
    });
    //POPULATE IT AGAIN
    thisNamespace.layouts.forEach(function (item) {
        $('#layouts').append($('<option>', {
                value: item,
                text: item
            }));
        $('#layoutsB').append($('<option>', {
                value: item,
                text: item
            }));
    });

    //$('#layouts').val(thisNamespace.layouts[0]);   //SET ACTIVE SLOT
    //$("#layouts").selectmenu("refresh");

    GetDbSelections(); //LOAD SELECTION FILES FOR PROJECT
}

function GetDbFileNames1() {

    //var requestTxt = {"name": name};
    //payload = JSON.stringify(requestTxt)
    path = dbprefix + '/api/namespace/summary';
    $.ajax({
        type: "GET",
        url: path,
        contentType: "application/json",
        //data: payload,
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        dataType: "json",
        success: function (response) {
            /////logger(response);
            // POPULATE UI DROPDOWN
            dbdata = response.slice(); //DEEP COPY !!!!
            logger(dbdata)
            $('#namespaces').find('option').remove().end();
            $('#namespaces').selectmenu('destroy').selectmenu({
                style: 'dropdown'
            });
            /*
            $('#layoutsB').append($('<option>', {value: "reeeeeee",text: "reeeeeee"}));

            response[0].layouts.forEach(function(item){
            //$('#layouts').append($('<option>', {value: item,text: item}));
            $('#layoutsB').append($('<option>', {value: item,text: item}));
            });

            // $('#layouts').val(response[0].layouts[0]);   //SET ACTIVE SLOT
            $('#layoutsB').val(response[0].layouts[0]);
            //$("#layouts").selectmenu("refresh");                          //AND SHOW
            $("#layoutsB").selectmenu("refresh");
            ///logger("REEEEEEEE");
             */
            response.forEach(function (item) {
                $('#namespaces').append($('<option>', {
                        value: item.namespace,
                        text: item.namespace
                    }));
            });

            $('#namespaces').val('ppi');
            $("#namespaces").selectmenu("refresh");

            UpdateNamespace('ppi');

        },

        error: function (err) {
            ///logger(err);

        }
    });
    //event.preventDefault();

}









function LogOnUIServer(data) {

    //var requestTxt = {"name": name};
    //payload = JSON.stringify(requestTxt)
    path = 'http://127.0.0.1:5000/print';

    $.ajax({
        type: "POST",
        url: path,
        contentType: "application/json",
        data: data,
        dataType: "json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        success: function (response) {

            /////logger(response);
        },
        error: function (err) {
            ///logger(err);
            /////logger(data);
        }
    });
    

}

function MyNewPostRequest(data) {

    payload = JSON.stringify(data);
    /////logger(payload);
    path = dbprefix + "/api/" + thisNamespace.namespace + "/MyNewRoute";
    $.ajax({
        type: "POST",
        url: path,
        contentType: "application/json",
        data: payload,
        dataType: "json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        success: function (response) {

            ///logger(response);
        },
        error: function (err) {
            ///logger(err);
            ///logger(data);
        }
    });

}





function GetDbNodeList1(name, channel) {

    path = dbprefix + "/api/" + thisNamespace.namespace + "/layout/" + name;
    $('#spinner_load').show();
    /*
    $('#projects-section').hide("drop", {
        direction: "down"
    }, "fast");
    */
    $.ajax({
        type: "GET",
        url: path,
        contentType: "application/json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        dataType: "json",
        success: function (response) {
            logger(response);
            if (channel == "A") {
                ue4("LoadDbNodeList", response);
                var globe = {"name":name};
                ue4("ShowGlobe", globe);
            } else if (channel == "B") {
                ue4("LoadDbNodeListB", response);
            }
            //logger(response);
            GetDbLabelList1(name, channel);
            
            $('#spinner_load').hide("drop", {
                direction: "down"
            }, "fast");
            /*
            $('#projects-section').show();
            /*             response.forEach(function(item){

            ///logger(item["a"][0])
            }); */
        },

        error: function (err) {
            ///logger(err);
            
            $('#spinner_load').hide("drop", {
                direction: "down"
            }, "fast");
            /*
            $('#projects-section').show();
            */
        }
    });
    //event.preventDefault();

}

function GetDbLinkList1() {

    path = dbprefix + "/api/" + thisNamespace.namespace + "/edge";
    $('#spinner_load').show();
    /*
    $('#projects-section').hide("drop", {
        direction: "down"
    }, "fast");
    */
    $.ajax({
        type: "GET",
        url: path,
        contentType: "application/json",

        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        dataType: "json",
        success: function (response) {
            ue4("LoadDbLinkList", response);
            $('#spinner_load').hide("drop", {
                direction: "down"
            }, "fast");
            logger(response);
            //$('#projects-section').show();
        },
        error: function (err) {
            $('#spinner_load').hide("drop", {
                direction: "down"
            }, "fast");
            //$('#projects-section').show();
            ///logger(err);
        }

    });
}

function GetDbLabelList1(name, channel) {

    path = dbprefix + "/api/" + thisNamespace.namespace + "/label/" + name;
    $.ajax({
        type: "GET",
        url: path,
        contentType: "application/json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        dataType: "json",
        success: function (response) {
            if (channel == "A") {
                ue4("LoadDbLabelList", response);
            } else if (channel == "B") {
                ue4("LoadDbLabelListB", response);
            }

            
            ///logger(response);
        },
        error: function (err) {
            ///logger(err);
        }
    });
}

////auto complete dynamic button factory
function GetDbSearchTerms(name, namespace) {

    if (namespace == "NODE") {
        path = dbprefix + "/api/" + thisNamespace.namespace + "/node?prefix=" + name;

        //api/ppi/node?prefix=as
        ///logger(path);
        if (name.length > 1) {
            $.ajax({
                type: "GET",
                url: path,
                contentType: "application/json",
                headers: {
                    "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
                },
                dataType: "json",
                success: function (response) {

                    response.sort(function (a, b) {
                        var x = a.symbol.toLowerCase(),
                        y = b.symbol.toLowerCase();
                        return x < y ? -1 : x > y ? 1 : 0;
                    });

                    clearButtons("autocomp");

                    response.forEach(function (item) {
                        /////logger(item.name + " " + item.symbol + " " + item.id + "autocomp");
                        createNodeButton(item.name, item.symbol, item.id, "autocomp");
                        // createNodeButton(response.nodes[i].name,response.nodes[i].symbol,response.nodes[i].node_id,"ResultList")
                        //$('#layouts').append($('<option>', {value: item,text: item}));
                    });

                    ///logger(response);
                },

                error: function (err) {
                    ///logger(err);

                }
            });
        }
    } else {
        path = dbprefix + "/api/" + thisNamespace.namespace + "/attribute/?prefix=" + name + "&namespace=" + namespace;
        ///logger(path);

        if (name.length > 1) {
            $.ajax({
                type: "GET",
                url: path,
                contentType: "application/json",
                headers: {
                    "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
                },
                dataType: "json",
                success: function (response) {

                    response.sort(function (a, b) {
                        var x = a.name.toLowerCase(),
                        y = b.name.toLowerCase();
                        return x < y ? -1 : x > y ? 1 : 0;
                    });

                    clearButtons("autocomp");

                    response.forEach(function (item) {
                        createButton(item.name, item.id, "autocomp");
                        //$('#layouts').append($('<option>', {value: item,text: item}));
                    });

                    ///logger(response);
                },

                error: function (err) {
                    ///logger(err);

                }
            });
            //event.preventDefault();
        }

    }

}

function createButton(Bname, Bid, Parent) {

    var r = $('<input/>').attr({
        type: "button",
        id: Bid,
        value: Bname

    });
    var p = '#' + Parent;
    $(p).append(r);
    $(r).button();
    $(r).click(function () {
        $("#searchInput1").text(Bname);
        $("#searchInput1").attr("searchID", Bid);
        // console.log(Bname + " " + Bid + " " + Parent);
        ue4("activateNode", Bid);
        //ONLY FOR WEB RESULTS VIEWER
        nodePanelRequest(Bid);
    });
}

function createNodeButton(Bname, Bsym, Bid, Parent) {
    //for resultList

    var r = $('<input/>').attr({
        type: "button",
        id: Bid,
        value: Bsym, //+ " - " + Bname
        //style: "color:#fc5a03"

    });
    var p = '#' + Parent;
    $(p).append(r);
    $(r).button();
    $(r).click(function () {
        $("#searchInput1").text(Bname);
        $("#searchInput1").attr("searchID", Bid);
        ue4("activateNode", Bid);
        // ///logger(Bid);
        //console.log(Bname + " " + Bid + " " + Parent);
    });
}

function createPubButton(Bname, Bid, Parent) {

    var r = $('<input/>').attr({
        type: "button",
        id: Bid,
        value: Bname

    });
    var p = '#' + Parent;
    $(p).append(r);
    $(r).button();
    $(r).click(function () {
       // $("#searchInput1").text(Bname);
       // $("#searchInput1").attr("searchID", Bid);
        console.log(Bname + " " + Bid + " " + Parent);
        publicationsAbstractRequest(Bid);

    });
}

function clearButtons(parent) {
    const myNode = document.getElementById(parent);
    while (myNode.firstChild) {
        myNode.removeChild(myNode.firstChild);
    }
}

//refresh selection dropdown

function GetDbSelections() {

    path = dbprefix + "/api/" + thisNamespace.namespace + "/attribute/?namespace=SELECTION";
    $.ajax({
        type: "GET",
        url: path,
        contentType: "application/json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        dataType: "json",
        success: function (response) {

            $('#selections').find('option').remove().end();
            $('#selections').selectmenu('destroy').selectmenu({
                style: 'dropdown'
            });

            response.forEach(function (item) {

                $('#selections').append($('<option>', {
                        value: item.id,
                        text: item.name
                    }));
            });

            //$('#selections').val( response[0].namespace);
            //$("#selections").selectmenu("refresh");

            ///logger(response);
        },

        error: function (err) {
            ///logger(err);

        }
    });
    //event.preventDefault();

}

function SimpleSearch(id) {

    path = dbprefix + "/api/" + thisNamespace.namespace + "/node/search?subject0=attribute&object0=" + id;
    ///logger(path);
    $.ajax({
        type: "GET",
        url: path,

        contentType: "application/json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        dataType: "json",
        success: function (response) {

            response.mode = $('#searchMode1').val();

            document.getElementById("sResults").innerHTML = "FOUND " + response.nodes.length + " NODES FOR " + $('#searchInput1').text();
            ue4("LoadSelectionDB", response);

            document.getElementById("ResultsLabel").innerHTML = "FOUND " + response.nodes.length + " NODES FOR " + $('#searchInput1').text();
            clearButtons("ResultList");

            /*             response.nodes.forEach(function(item){

            }); */

            response.nodes.sort(function (a, b) {
                var x = a.symbol.toLowerCase(),
                y = b.symbol.toLowerCase();
                return x < y ? -1 : x > y ? 1 : 0;
            });

            for (var i = 0; i < 400 && i < response.nodes.length; i++) {

                createNodeButton(response.nodes[i].name, response.nodes[i].symbol, response.nodes[i].node_id, "ResultList");

            }
            ///logger(response);

        },

        error: function (err) {
            ///logger(err);

        }
    });
    //event.preventDefault();

}

function SaveSelectionDB(data) {

    payload = JSON.stringify(data);
    ///logger("saveSelectionDB says:");
    ///logger(payload);
    path = dbprefix + "/api/" + thisNamespace.namespace + "/selection/create";
    $.ajax({
        type: "POST",
        url: path,
        contentType: "application/json",
        data: payload,
        dataType: "json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        success: function (response) {

            ///logger(response);
        },
        error: function (err) {
            ///logger(err);
            ///logger(data);
        }
    });
    //event.preventDefault();
}

function LoadSelectionDB(id) {

    path = dbprefix + "/api/" + thisNamespace.namespace + "/node?attribute_id=" + id;
    /////logger(path);
    $.ajax({
        type: "GET",
        url: path,
        contentType: "application/json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        dataType: "json",
        success: function (response) {

            response.mode = $('#selectMode').val();
            ue4("LoadSelectionDB", response);
            ///logger(response);

            var nodes = response;
            var jsonObj = {nodes:[],mode:"NEW"};


            jsonObj.nodes = nodes;
            jsonObj.mode = $('#selectMode').val();
            ///logger(JSON.stringify(jsonObj));

            // document.getElementById("sResults").innerHTML = "FOUND " + response.nodes.length + " NODES FOR " + $('#searchInput1').text();
            // ue4("LoadSelectionDB", response);

            // document.getElementById("ResultsLabel").innerHTML = "FOUND " + response.nodes.length + " NODES FOR " + $('#searchInput1').text();
            // clearButtons("ResultList");


            // for (var i = 0; i < 100 && i < response.nodes.length ; i++) {

            // createNodeButton(response.nodes[i].name,response.nodes[i].symbol,response.nodes[i].node_id,"ResultList");

            // }


        },

        error: function (err) {
            ///logger(err);

        }
    });
    //event.preventDefault();

}

function GetNodesForAttributes(instring) {

    path = dbprefix + "/api/" + thisNamespace.namespace + "/node?" + instring;

    ///logger(path);
    $.ajax({
        type: "GET",
        url: path,

        contentType: "application/json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        dataType: "json",
        success: function (response) {
            ///logger(response);
            // response.mode = $('#searchMode1').val();

            // document.getElementById("sResults").innerHTML = "FOUND " + response.nodes.length + " NODES FOR " + $('#searchInput1').text();
            // ue4("LoadSelectionDB", response);

            // document.getElementById("ResultsLabel").innerHTML = "FOUND " + response.nodes.length + " NODES FOR " + $('#searchInput1').text();
            // clearButtons("ResultList");

            /*             response.nodes.forEach(function(item)
        {

            }); */
            document.getElementById("pseeds").innerHTML = "SEEDS - FOUND " + response.nodes.length + " NODES ";

            response.nodes.sort(function (a, b) {
                var x = a.symbol.toLowerCase(),
                y = b.symbol.toLowerCase();
                return x < y ? -1 : x > y ? 1 : 0;
            });

            $("#seedbox").empty();
            for (var i = 0; i < 100 && i < response.nodes.length; i++) {

                createNodeButton("", response.nodes[i].symbol, response.nodes[i].node_id, "seedbox");

            }

        },

        error: function (err) {
            ///logger(err);

        }
    });
    //event.preventDefault();

}

function ReLayoutSubSet(data) {

    //console.log(data);
    var dummydata = {
        "node_ids": []
    };
    dummydata.node_ids = data.node_ids;
    //console.log(JSON.stringify(data.node_ids));
    payload = JSON.stringify(dummydata);
    console.log(payload);
    //
    path = dbprefix + "/api/" + thisNamespace.namespace + "/node/sub_layout";
    $.ajax({

        type: "POST",
        url: path,
        contentType: "application/json",
        data: payload,
        dataType: "json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        success: function (response) {

            logger(response);
            ue4("reLayout", response);
        },
        error: function (err) {
            logger(err);

        }
    });
    //event.preventDefault();
}


 

function GSEASubSet(data) {

    //console.log(data);
    var dummydata = {
        "node_ids": [],
        "annotation":"ALL"
    };
    dummydata.node_ids = data.node_ids;
    dummydata.annotation = data.selection_name;
    //console.log(JSON.stringify(data.node_ids));
    payload = JSON.stringify(dummydata);
    //console.log(payload);
    //
    path = dbprefix + "/api/" + thisNamespace.namespace + "/node/gsea";
    $.ajax({

        type: "POST",
        url: path,
        contentType: "application/json",
        data: payload,
        dataType: "json",
        headers: {
            "Authorization": "Basic " + btoa(dbuser + ":" + dbpw)
        },
        success: function (response) {

            logger(response);
            //ue4("reLayout", response);
            drawGSEABarChart(response);
        },
        error: function (err) {
            ///logger(err);

        }
    });
    //event.preventDefault();
}







function ExportPdf() {
    kendo.drawing
    .drawDOM("#tabs-1", {
        paperSize: "A4",
        margin: {
            top: "1cm",
            bottom: "1cm"
        },
        scale: 0.8,
        height: 500
    })
    .then(function (group) {

        kendo.drawing.pdf.saveAs(group, "Exported.pdf")
    });
    ///logger("saving");
}