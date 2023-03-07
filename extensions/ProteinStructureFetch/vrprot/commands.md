# Building and uploading project

## build pypi - project

`cd pypi_project`

- clear dist folder before building a new version of the project.

`rm -rf dist`

`python3 -m build`

## upload pypi - project

`python3 -m twine upload dist/*`
`python3 -m twine upload --repository testpypi dist/*`

- New version number in pyproject.toml when uploading a new version of the project.

username = \_\_token\_\_

password = <API_TOKEN>

To install project from test.pypi.org:

`pip install -i https://test.pypi.org/simple/ vrprot`

# Building one-file executable

`pip install pyinstaller`
`pyinstaller --onefile AlphaFoldVRNetzer.py`
