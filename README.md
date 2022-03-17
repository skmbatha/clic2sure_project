# 1. Environment setup

## Setting up the environment

To run the project, a virtual environment must be created and the following packages should be installed using the the Python PIP tool. Alternatively, teh project can run but these modules should be installed (System wide).

* Django==4.0.3
* djangorestframework==3.13.1
* docutils==0.18.1
* factory-boy==3.2.1

## Running the backend through the "Django dev server"

This project was developed and tested on the dev server.
The dev server can be started by running the command (specified below) from the project root
(where the manage.py file resides). Please note that depending on the version
of python you have installed you might have to use ```python3``` instead of ```python``` in the
commands.

THE DEVSERVER runs at port 8000 by default, but pass in the option to be ensure it does.

```
python manage.py runserver 8000
```


## Running at port 8000

Please run the project at port 8000. The reason for this is that:

* The Test cases in ***/app/tests.py*** refer to (http://localhost:8000/) for all the API tests.
* The CURL example commands documented in ***/CURL and API mapping/CURL Communication and API map.pdf*** use (http://localhost:8000/).
* The admin page can be accessed from the browser using the same link+ port (http://localhost:8000/admin/)


Otherwise, you must manually change the port in the code...which you should probably NEVER do!!!


##  Authentication method

This project uses a Token based authentication method. Most of the API routes are protected and need the user to pass in a token received after a successful login. Only the ***/createuser/*** and ***/login/*** routes are unprotected. The token should be passed into the request header. For example, if the token received is _123456789_, the header should have _Authorization: Token 12345789_. This information is also explained in the PDF document ***/CURL and API mapping/CURL Communication and API map.pdf***.



# 2. Docs, API Map and CURL

## Documentation

The code is extensively documented using \_\_doc\_\_ strings. The module ***PyDoc*** was used to generate HTML docs for all the (.py) files in the ***/app/\**** directory. All the docs are in seperate files for each python file and stored in ***/docs/\****


## API mapping

The API mapping is tabulated and described in _Table 1_ of the PDF document ***/CURL and API mapping/CURL Communication and API map.pdf***. 


## CURL commands

The use of CURL commands and how they are communicate with the backend API is described in _Table 2_ of the PDF document ***/CURL and API mapping/CURL Communication and API map.pdf***. The enumerated list in _Table 1_ and _Table 2_ correlate. This means, row 1 in in _Table 1_ corresponds to the CURL version in _Table 2_.




# 3. Running tests

The Unit tests inherit from the Django Rest Framework APITestCase class. These test's \_\_doc\_\_ strings provide information on what requirement per the supplied project definition document (PDD) the test case is testing. The test function names are also self explanatory. Furthermore, the ***/docs/app.test.html***  can be used to find the test case information. Comments are embedded in the code for further clarity.

To perform a test run, open two terminals both in the project root (where the manage.py file resides).
First start the server by issuing this command in _Terminal 1_:

```
python manage.py runserver 8000
```

then run the following command in _Terminal 2_ to run perform a test run,

```
python manage.py test
```

The tests results will show in _Terminal 2_.




# 4. Populating DB with dummy data

In the project the script to perform a randomized data loading into the DB is a command. The command python file is placed in ***/app/management/commands/setup_test_data.py***. This commands uses ***/app/factories.py***
which is a class that uses the native python ```factory``` and ```factory.django``` packages to dynamically generate dummy data. The command performs 5 operations:

* Deletes all records from the database for all tables except for the superuser account in the User table.
* Creates new 5 dummy users using ```UserFactory``` class defined in ***/app/factories.py***.
* Creates new 30 savings accounts for random existing users using ```SavingsAccountFactory``` class defined in ***/app/factories.py**.
* Creates new 20 credit accounts for random existing users using ```CreditAccountFactory``` class defined in ***/app/factories.py**.
* Creates new 100 transactions for random users and acccounts using```TransactionFactory``` class defined in ***/app/factories.py**.

To run the dummy data creation and population, run the following command from the project root (where the manage.py file resides).


```
python manage.py setup_test_data
```

# 5. Admin page

The admin page was not implemented exactly per Requirement 8 in the project definition document because of time contraints. However a native django admin site is used to display the following database models

* A list of all users
* A list of all users' authentication tokens
* A list of all Savings accounts and their respective users
* A list of all Credit accounts and their respective users.
* A list of all transactions for all accounts adn for all users.

To login to the admin site, run the dev_server by issuing this command

```
python manage.py runserver 8000
```

, then open any local browser and open the link : (http://localhost:8000/admin/). This should
land you on the admin login page. The login credentials for the admin are:

* Username : _admin_
* Password : _admin_



# 6. Downloading the CSV file

The CSV file per Requirement 9 in the project definition document can be downloaded by 1st running the dev server as shown above and then entering the download link (http://localhost:8000/csv/) in any local browser's URL field. When submited, the CSV file will download.


