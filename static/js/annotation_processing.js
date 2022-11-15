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

vRNetzer.annotation.func.clearAnnotationName = function(name){
    // function to remove id from name to get clear name, assuming name = "id;clearName"
};

vRNetzer.annotation.func.setUnion = function(arr1, arr2){
    return Array.from(new Set([...arr1, ...arr2]));
};

vRNetzer.annotation.func.setIntersect = function(arr1, arr2){
    return new Array([...arr1].filter(item => arr2.has(item)));
};

vRNetzer.annotation.func.setSubtract = function(arr1, arr2){
    let result = [];
    arr1.forEach(function(item){
        if (!arr2.has(item)){
            result.push(item);
        }
    });
    return result;
};

vRNetzer.annotation.func.debugShowPreview = function(project){
    let url = "/preview?project=" + project + "&render-annotation=true";
    window.open(url, '_blank').focus();
};

vRNetzer.annotation.func.generateAnnotationTexture = function(){};

vRNetzer.annotation.func.renderAnnotationTexture = function(nodesObject, arr1, arr2, node, operator){
    console.log("Annotation: render new Texture: ", node, operator);
};
