function variableListener(obj) {
  var keys = Object.keys(obj);
  newListnerObject = {};
  for (var i = 0; i < keys.length; i++) {
    var key = keys[i];
    var value = obj[key];
    if (value == undefined) {
      continue;
    }
    newListnerObject = addListener(newListnerObject, key, obj[key]);
  }
  return newListnerObject;
}

function addListener(obj, key, value) {
  if (isJsonObject(value)) {
    value = variableListener(value);
  }
  obj[key + "Internal"] = value;
  obj[key + "Listener"] = function (val) {
    // console.log("updated:\n" + val);
  };
  Object.defineProperty(obj, key, {
    set: function (val) {
      this[key + "Internal"] = val;
      this[key + "Listener"](val);
    },
    get: function () {
      return this[key + "Internal"];
    },
  });

  obj[key + "RegisterListener"] = function (new_function) {
    this[key + "Listener"] = (function (old_function, new_function) {
      function extendedFunction(val) {
        old_function(val);
        new_function(val);
      }
      return extendedFunction;
    })(this[key + "Listener"], new_function);
  };
  return obj;
}

function isJsonObject(obj) {
  if (typeof obj !== "object" || obj === null || Array.isArray(obj)) {
    return false;
  }
  try {
    JSON.stringify(obj);
    return true;
  } catch (e) {
    return false;
  }
}
