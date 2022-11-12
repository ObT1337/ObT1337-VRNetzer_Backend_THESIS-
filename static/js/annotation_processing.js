// ##########################################################
// Processing script for annotation analyzer tab in main.html
// ##########################################################


// fucntions
function buildAnnotationMap(nodes){
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
}

function clearAnnotationName(name){
    // function to remove id from name to get clear name, assuming name = "id;clearName"
}

function setUnion(arr1, arr2){
    return Array.from(new Set([...arr1, ...arr2]));
}

function setIntersect(arr1, arr2){
    return new Array([...arr1].filter(item => arr2.has(item)));
}

function setSubtract(arr1, arr2){
    let result = [];
    arr1.forEach(function(item){
        if (!arr2.has(item)){
            result.push(item);
        }
    });
    return result;
}

function debugShowPreview(project){
    let url = "/preview?project=" + project + "&render-annotation=true"
    window.open(url, '_blank').focus();
}

function generateAnnotationTexture(){}

function renderAnnotationTexture(nodesObject, arr1, arr2, node, operator){
    console.log("Annotation: render new Texture: ", node, operator);
}
