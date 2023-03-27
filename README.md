# DISCLAIMER

This repository is a frozen version of the VRNetzer backend used in my thesis. It is not maintained anymore and is only kept for archival purposes.
For the current version of the VRNetzer Backend, please refer to the [VRNetzer](https://github.com/menchelab/VRNetzer) repository (Prich et. al 2021).

# VRNetzer Backend

This is a flask server that provides the network data to the UnrealEngine VRNetzer VR Clients

## Installation

1. Start the backend

   - install python 3.9 +
   - on Windows: run `Buildandrun.ps` in console.
   - on Linux: run `linux_buildandrun.sh` in console.
   - on macOs: run `linux_buildandrun.sh` in console.

   If all dependencies installed correctly, the console should show </br>

   ```
   ==================================================
   Finished loading extensions, server is running...
   ```

   As the port 5000 is already occupied by the systems control center, on mac the server will run on port 3000 (instead of 5000).

2. Upload data and create a new project

   - open a browser (Chrome or Firefox) and go to [127.0.0.1:5000/upload](http://127.0.0.1:5000/upload) / [127.0.0.1:3000/upload](http://127.0.0.1:3000/upload)(mac)
   - make sure "create new project" is checked and assign a name
   - choose a layout file from "static/csv" (or more) or use your own
   - pick a link file from "static/csv" (same name as above) or use your own
   - click upload

   After a success message was shown, the uploader has now created a new folder in "static/projects/yourprojectname" containing all the data in the VRNetzer format.

3. Use the WebGL preview to have a look at your project without having to use VR hardware

   - go to [127.0.0.1:5000/preview](http://127.0.0.1:5000/preview) / [127.0.0.1:3000/upload](http://127.0.0.1:3000/upload)(mac)
   - select your project from the dropdown

4. run the VR

   Available on request (contact: [till@menchelab.com](mailto:till@menchelab.com))

## Extensions

To install an extension the respective extension can be added to the `extension` directory. For further installation procedures please refer to the respective extension's ReadMe file.

## Feedback and Questions

If you have any questions or feedback, don't hesitate to contact me via email [till@menchelab.com](mailto:till@menchelab.com) or refer to the [VRNetzer](https://github.com/menchelab/VRNetzer) repository (Prich et. al 2021).
