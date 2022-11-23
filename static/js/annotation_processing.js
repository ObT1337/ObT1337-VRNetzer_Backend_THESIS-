// ##########################################################
// Processing script for annotation analyzer tab in main.html
// ##########################################################


// create namespace
var vRNetzer = vRNetzer || {};
vRNetzer.annotation = vRNetzer.annotation || {};
// namespace for variables
vRNetzer.annotation.vars = vRNetzer.annotation.vars || {};
// namespace for functions 
vRNetzer.annotation.func = vRNetzer.annotation.func || {};


vRNetzer.annotation.func.buildAnnotationMap = function(nodes){
    // return map: annotation:[nodes]
    outMap = new Map();
    for (let i = 0; i < nodes["nodes"].length; i++){
        nodes["nodes"][i]["annotation"].forEach(function(item){
            if (!outMap.has(item)){
                outMap.set(item, []);
            };
            outMap.get(item).push(nodes["nodes"][i]["n"]);
        })
    }
    return outMap;
};


vRNetzer.annotation.func.setUnion = function(arr1, arr2){
    return Array.from(new Set([...arr1, ...arr2]));
};

vRNetzer.annotation.func.setIntersect = function(arr1, arr2){
    return new Array([...arr1].filter(item => arr2.includes(item)));
};

vRNetzer.annotation.func.setSubtract = function(arr1, arr2){
    let result = [];
    arr1.forEach(function(item){
        if (!arr2.includes(item)){
            result.push(item);
        }
    });
    return result;
};


vRNetzer.annotation.func.generateAnnotationTexture = function(highlight, project){
    socket.emit("request", {id: "requestAnnotationHighlight", project: project, data: highlight})
};

vRNetzer.annotation.func.renderAnnotationTexture = function(nodesTexturePath, linksTexturePath, project){
    // after receiving response from texture generator: send texture to preview & ue
    console.log("Annotation: render new node texture: " + nodesTexturePath + " ; new links texture: " + linksTexturePath + " ; in project: " + project);
    /* 
    
    SOCKET CONNECTION TO UE4 here to switch textures
    
    */

    // display in preview webGL window
    let suffixURL = window.location.href.split('/')[0];
    let previewURL = "/preview?project=" + project + "&layout=0&ncol=0&lcol=0&annotation-nodes=" + nodesTexturePath + "&annotation-links=" + linksTexturePath;
    
    window.open(suffixURL + previewURL, '_blank').focus();
};

vRNetzer.annotation.func.renderBaseTexture = function(project){
    // render basic texture in preview & send to ue
    /* 
    
    SOCKET CONNECTION TO UE4 here to switch textures
    
    */

    // display in preview webGL window
    let suffixURL = window.location.href.split('/')[0];
    let previewURL = "/preview?project=" + project + "&layout=0&ncol=0&lcol=0";
    window.open(suffixURL + previewURL, '_blank').focus();
};