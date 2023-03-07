# VRNetzer backend example extension

This series teaches you the basic skills you need for developing an extension for the VRNetzer backend module.

<h1> Overview </h1>

Here you will get an overview of the VRNetzer platform. You will learn what you can do with the VRNetzer platform and how to use it. Furthermore, you will learn about the essential technical aspects of the VRNetzer platform.

### What is the VRnetzer?

The VRNetzer is a virtual reality platform used to explore and analyze network data.

## Useful Presentations and Tutorials

In the following you can find some resources that might be useful for you:
| Resource | Description | Reference |
| --- | --- | --- |
| SOME INTRODUCTION | SOME DESCRIPTION | SOME REFERENCE |
| SOME INTRODUCTION | SOME DESCRIPTION | SOME REFERENCE |
| SOME INTRODUCTION | SOME DESCRIPTION | SOME REFERENCE |
| SOME INTRODUCTION | SOME DESCRIPTION | SOME REFERENCE |
| SOME INTRODUCTION | SOME DESCRIPTION | SOME REFERENCE |

### Get in touch

If you would like to discuss anything about the VRNetzer, you can join our community, contact us directly via email or visit our website.
| Platform | Description | Reference |
| --- | --- | --- |
|(EMAIL/WEBSITE/SOCIALMEDIA)| SOME DESCRIPTION | SOME REFERENCE |
|(EMAIL/WEBSITE/SOCIALMEDIA)| SOME DESCRIPTION | SOME REFERENCE |
|(EMAIL/WEBSITE/SOCIALMEDIA)| SOME DESCRIPTION | SOME REFERENCE |
|(EMAIL/WEBSITE/SOCIALMEDIA)| SOME DESCRIPTION | SOME REFERENCE |
|(EMAIL/WEBSITE/SOCIALMEDIA)| SOME DESCRIPTION | SOME REFERENCE |

### The technology behind the VRNetzer

The VRNetzer 2.0 ...

- Running on Flask 2.0
- UI HTML/CSS/JS

### Extension of VRNetzer Core

The Core module builds the basis of the VRNetzer. It comes with a basic set of features to
visualize network data. We highly encourage you to extend the VRNetzer and share your results with the community. This way, you can help us to improve the VRNetzer and make it more useful for everyone.

<h1> Start creating your first extension</h1>

### Fork the VRNetzer backend repository

To create a testing environment for your extension you should start by creating a fork of the [VRNetzer backend repository](https://github.com/menchelab/VRNetzer_Backend). This way, you can include your extension in the VRNetzer backend and test it. Furthermore, you can easily keep track of the changes we make to the VRNetzer backend and update your extension accordingly if needed.

### Fork the ExampleExtension repository

To easily share your extension with the community, we recommend creating a fork of the [ExampleExtension repository](https://github.com/menchelab/ExampleExtension). This way you can easily update, and change your extension, as well as keep track of issues. Furthermore, everyone who would like to use it can drop it into their VRNetzer backend without fetching the full backend module.

### Add your extension to the VRNetzer backend

Now that you forked both the VRNetzer backend as well as the ExampleExpansion, you can start by cloning your forked repository of the VRNetzer backend to your desired location.

    git clone https://github.com/<YourGitUsername>/VRNetzer_Backend

Subsequently, you can add your forked ExampleExtension as a submodule to your VRNetzer backend.:

    cd VRNetzer_Backend

    cd extensions

    git submodule add https://github.com/<YourGitUsername>/ExampleExtension.git

In this manner, you can easily change your extension while keeping it contained in the testing environment of the VRNetzer backend. Whenever you change something in your extension, you can easily commit your changes to your forked ExampleExtension repository.

<ins>**Tip** </ins>

If the directory of your submodule is for some reason empty you can use the following command to sync the submodules

    git submodule sync

or use

    git submodule update --init --recursive

### Run the VRNetzer with your extension

The ExampleExtension repository gives you a basic idea of what is needed so that your extension can be loaded by the VRNetzer backend. To test your extension, you can simply run the VRNetzer backend running the appropriate script for your platform:

- windows: run `buildandRUN.ps1` in console
- linux: run `linux_buildandrun.sh` in console
- mac: run `mac_buildandrun.sh` in console

This script will create a virtual environment, install all necessary dependencies and run the VRNetzer backend. If everything worked out, you should see the following message in green in your console:

> <span style="color:green"> Loaded extension: ExampleExtension<br>
> Finished loading extensions, server is running...</span>

If you see a yellow warning message similar to this:

> <span style="color:yellow">
> Traceback (most recent call last):<br>
> File "/VRNetzer_Backend/load_extensions.py", line 17, in load<br>
> &nbsp;&nbsp;module.blueprint, url_prefix=module.url_prefix<br>
> &nbsp;&nbsp;&nbsp;&nbsp;AttributeError: module 'extensions.documentation.src.app' has no attribute 'blueprint'<br><br>
> Make sure you have an app.py file in the '/src/' folder of your extension.
> <br>
> Make sure that you have defined a 'url_prefix' for your in the app.py file.
> <br>
> Make sure your flask blueprint is called 'blueprint'.
> </span>

<br>

something seems to be wrong with your extension and it will not be loaded by the flask server. You can check [here](#troubleshooting) for possible solutions.

### Components of an extension

The ExampleExtension repository gives you a basic idea of what is needed so that your extension can be loaded by the VRNetzer backend. In the following, we will give you a more detailed overview of the components of an extension.

**1. `app.py` file in an `src` directory**

The app.py file is the entry point of your extension. It has to be included in a directory called "src" in the home directory of your Extension. The app.py file has to contain the following attributes:

- A string called `url_prefix`.

  - This string defines the prefix each flask route of your extension will have. For example, if you set the url_prefix to 'example', the route '/test' will be accessible via 'http://localhost:5000/example/test'.

- A flask blueprint or an IOBlueprint called `blueprint`.

  - this attribute is defined by the following line of code:

  ```
  blueprint = flask.Blueprint(
      extensions_name,
      __name__,
      url_prefix=url_prefix)
  ```

  or

  ```
  from io_blueprint import IOBlueprint
  blueprint = IOBlueprint(
      extensions_name,
      __name__,
      url_prefix=url_prefix)
  ```

  The blueprint will be registered by the main VRNetzer backend `app.py` and is used to define the routes your extension adds. For further information on flask blueprints, you can check the [flask documentation](https://flask.palletsprojects.com/en/2.0.x/blueprints/). The IOBlueprint is a custom blueprint class that allows extensions to send and receive socket io messages.

---

**2. Include templates and static files which are specific to your Extension**

To make templates and static files contained in your extension accessible, it has to be defined, where they can be found. We suggest adding two directories named templates and static to your extension to be consistent with Flask's naming convention.
During the initialization of the blueprint, the following lines of code guide the Flask server to the correct directories:

```
templates =  os.path.abspath("./extensions/<NameOfYourExtension>/templates")

static = os.path.abspath("./extensions/<NameOfYourExtension>/static")

blueprint = flask.Blueprint( # Or IOBlueprint
    <NameOfYourExtension>,
    __name__,
    url_prefix=url_prefix,
    template_folder=templates, # defaults to static of main app.py
    static_folder=static, # defaults to static of main app.py
)
```

To link to files in these directories in your HTML files, you should utilize flask's `url_for` function. For example, if you want to link to a file called `style.css` in your `"<NameOfYourExtension>/static/css"` directory, you can use the following line of code:

```
"{{ url_for('<NameOfYourExtension>.static', filename='css/style.cs') }}"
```

---

**3. Add functions to be executed before the first request**

If some function needs to be executed before the first request, you can decorate this function with the decorator `@blueprint.before_app_first_request` in your app.py.

```
@blueprint.before_app_first_request
def extension_setup():
    # Your code
    pass
```

This tells the main app to execute this function just before the first request is made. This is useful if you want to initialize some variables or load some data before the first request is made.

---

**4. Add tabs to the Main Panel and add a new Uploader**

If you want to add a new tab to the VRNetzer Main Panel, you can utilize the `example_main_tab.html` template contained in the ExampleExtension. Each HTML that should be added as a tab to the main panel, has to be added to the `main_tabs`list in the `app.py` file. The flask server will automatically add the tabs to the main panel.
The content of the tab needs to be contained in a `div` with the id `tab_to_add`:

```
<div id="tab_to_add" class="container" style="display:none;">
    <div id="example_tab">
      <!-- Your Content -->
    </div>
</div>
```

On each request, the flask sever will add your tab to the main panel. If you want to change the icon on the tab, you have to define an `image` tag with the id `tab_icon` in your tab template. The src of this image will contain the URL for the icon you want to use.

```
<img id="tab_img" src="{{ url_for('ExampleExtension.static', filename='img/example_icon.png') }}"
style="display: none;" ;>
```

The flask server will change the icon accordingly. Furthermore, external links to stylesheets and scripts will automatically be added to the main HTML header. Every other code contained in the HTML tab will also be added to the main HTML file.

All of this applies if you want to add a new tab to the uploader. You can utilize the `example_upload_tab.html` template contained in the ExampleExtension. HTML files to add have to be added to the `upload_tabs` list in the `app.py` file.

If you want to add a new tab to the nodepanel or nodepanelppi, you can utilize the `example_nodepanel_tab.html` and `example_nodepanelppi_tab.html` template contained in the ExampleExtension. HTML files to add have to be added to the list `nodepanel_tabs` and `nodepanelppi_tabs`, respectively, in the `app.py` file.

<h4 id="home_present"><b>5. Present your new routes at VRNetzer's Home</h4>

If you want your route to be presented in one of the categories shown on http://127.0.0.1:6000/home (Windows/Linux) / http://127.0.0.1:3000/home (MacOS), your route has to contain one of the following keywords:
|Keyword|Category|Example|
|:-|:-|:-|
|`main`|Main (Panels)|`@blueprint.route("/main")`|
|`nodepanel`|Node Info|`@blueprint.route("/nodepanel")`|
|`upload` but not `upload` and `files`|Uploader|`@blueprint.route("/upload")`|
|`preview`|Previews|`@blueprint.route("/preview")`|

**6. Perform socketio.emit from extension**

To send a `socketio.emit` from your extension, your blueprint has to be an IOBlueprint. Then you can use the following code to emit a socketIO message in your namespace:

```
blueprint.emit(
    "ex",
    {"id": "someId", "opt": "someOption", "fn": "someFunction"},
)
```

If you want to emit a message to namespace, your can use the namespace argument:

```
namespace="/chat"
room = flask.session.get("room")
blueprint.emit(
    "ex",
    {"id": "someId", "opt": "someOption", "fn": "someFunction"},
    room = room,
    namespace = namespace,
)
```

**6. Receive a socket io message for your extension namespace**

```
@blueprint.on("example")
def example_receive_socketio(message):
    print("Received example form client:")
    print(message)
```

You can also provide a different namespace for example `/chat`:

```
@blueprint.on("example",namespace="/chat")
def example_receive_socketio_in_main(message):
    print("Received example form client:")
    print(message)
```

This can be useful if your extension adds new UI elements to the main panel and you want to send a message to your extension.

<!--
## Deployment

## TODO: Describe the deployment process on a platform where you can present your extension.
-->

<h1> Further Resources </h1>
<h2 id="example_ext"> Example Extensions </h2>
To get an idea of how an extension can be structured, you can check out the following example extensions:

| Extension             | Description                                                                                                                                                         | Link                                                       |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| StringEx              | This extension is designed to present [STRING DB](https://string-db.org/) networks on the VRNetzer platform.                                                        | [Link](https://github.com/menchelab/StringEx)              |
| ProteinStructureFetch | This extension allows for fetching and processing 3d protein structures from [AlphaFold DB](https://alphafold.ebi.ac.uk/) to explore them on the VRNetzer platform. | [Link](https://github.com/menchelab/ProteinStructureFetch) |

---

<!--
<h2 id="troubleshooting"> Troubleshooting </h2>
TODO: list common problems and solutions
-->

```

```
