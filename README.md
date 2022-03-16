# 1. Environment setup

## Setting up the environment

To run the project, a virtual environment could be created and the following packages should be installed using the the Python PIP tool.

* Django==4.0.3
* djangorestframework==3.13.1
* docutils==0.18.1
* factory-boy==3.2.1

## Running the backend through the "Django dev server"

This project was developed and tested on the dev server.
The dev server can be started by running the command from the project root
(where the manage.py file resides). Please note that depending on the version
of python you have installed you might have to use python3 instead of pythn in the
command below.

THE DEVSERVER runs at port 8000 by default, but pass in the option to be sure.

```
python manage.py runserver 8000
```


## Running at port 8000

Please run the project at port 8000. The reason for this is that:

* The Test cases in ***/app/tests.py*** refer to (http://localhost:8000/) for all the API tests.
* The CURL exaple commands documented in ***/CURL and API mapping/CURL Communication and API map.pdf*** are use the (http://localhost:8000/)
* The admin page can be accessed from the browser using the same link port (http://localhost:8000/admin/)

Otherwise, you must manually change the port in the code...which you should probably NEVER do.!

# 2. Docs, API Map and CURL

## Documentation

The code is extensively documented using DOC_STRINGS. The module PyDoc was used to generate HTML docs for all the (.py) files in the ***/app/\**** directory. All the docs are in seperate files for each python file and stored in ***/docs/\****


## API MAP

The API mapping to the program features/functions is tabulated and described in the PDF document [API MAP and CURL defs](docs/CURL Communication and API map.pdf)