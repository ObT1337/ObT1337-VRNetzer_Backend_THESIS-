# VRNetzer Backend

This is a flask server that provides the network data to the UnrealEngine VRNetzer VR Clients

## INSTALLATION

1) run backend
    - install python 3.9 plus
    - windows: run ```Buildandrun.ps``` in console
    - mac/linux: run ```linux_buildandrun.sh``` in console
    
    If all dependencies installed correctly, the console should show </br>
    `The server is now running at 127.0.0.1:5000`

2) upload data and create new project
    - open a browser (Chrome or Firefox) and go to [127.0.0.1:5000/upload](http://127.0.0.1:5000/upload)
    - make sure "create new project" is checked and assign a name 
    - choose a layout file from "static/csv" (or more) or use your own
    - pick a link file from "static/csv" (same name as above) or use your own
    - click upload

    After a success message was shown, the uploader has now created a new folder in "static/projects/yourprojectname" containing all the data in the VRNetzer format.

3) use the WebGL preview to have a look at your project without having to use VR hardware
    - go to [127.0.0.1:5000/preview](http://127.0.0.1:5000/preview)
    - select your project from the dropdown

4) run the VR
    you need:
    - a VR ready windows computer
    - a SteamVR compatible headset
    - SteamVR installed
    - download the VRNetzer executable
    - open "VRNetzer/Colab/Content/data/config.txt and make sure it contains the adress the VRNetzer backend is running at
    - run VRnetzer.exe


## DOCUMENTATION

<details>
  <summary><h3> VRNetzer Dataformat</h3></summary>
    
The VRNetzer acts as a multiplayer gameserver for one or more VR clients.
Its purpose is to serve the connected players with big network datasets - as quickly as possible.
That is the reason why most properties are stored (and transmitted over the network) as images.



Every folder in "static/projects/ contains 3 JSON files (check out the file dataframeTemplate.json for the exact structure)
as well as 5 subfolders containing textures
    
- static/projects/projectname/
    - nodes.json
    - links.json
    - pfile.json
    - layouts  
    - layoutsl 
    - layoutsRGB
    - links 
    - linksRGB   


layouts + layoutsl -> Node Positions

this needs a little explaining:
Think as a texture as a dataset of the following format: [[R,G,B],[R,G,B],[R,G,B],..] where every [R,G,B] is a pixel.
This can be used to store a location (X->R Y->G Z->B) per pixel.
Because a .bmp only has 8 bit depth we need a second texture to get a resolution of 65536 per axis. this is where "layoutsl" comes into play.
NOTE: node positions need to be in a 0 - 1 range (!), the conversion works like this:

floor(x * 256) -> layouts
floor(x * 65536 % 256) -> layoutsl

| Column 1 Header | Column 2 Header | Column 3 Header |
| --------------- | --------------- | --------------- |
| Row 1 Column 1 | Row 1 Column 2 | Row 1 Column 3 |
| Row 2 Column 1 | Row 2 Column 2 | Row 2 Column 3 |
| Row 3 Column 1 | Row 3 Column 2 | Row 3 Column 3 |


</details>

