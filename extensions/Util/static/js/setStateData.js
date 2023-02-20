$(document).ready(function () {
  // Load StateData
  if (pdata.stateData.layout) {
    $("#layouts").val(pdata.stateData.layout);
    $("#layouts").selectmenu("refresh");
  }
  if (pdata.stateData.layoutRGB) {
    $("#nodecolors").val(pdata.stateData.layoutRGB);
    $("#nodecolors").selectmenu("refresh");
  }
  if (pdata.stateData.linkl) {
    $("#links").val(pdata.stateData.linkl);
    $("#links").selectmenu("refresh");
  }
  if (pdata.stateData.linkRGB) {
    $("#linkcolors").val(pdata.stateData.linkRGB);
    $("#linkcolors").selectmenu("refresh");
  }
  if (pdata.stateData.main_tab) {
    $("#tabs").tabs("option", "active", pdata.stateData.main_tab);
  }
});
