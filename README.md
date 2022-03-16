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


##  Authentication method

This project uses a Token based authentication methods. All request are protected and need the user to pass in a token received after a successful login into the header. For example if token received is _123456789_, the header shoul dbe _Authorization: Token 12345789_. This information is already explained in the PDF document ***/CURL and API mapping/CURL Communication and API map.pdf***  as described in section 2 of this document. 



# 2. Docs, API Map and CURL

## Documentation

The code is extensively documented using DOC_STRINGS. The module PyDoc was used to generate HTML docs for all the (.py) files in the ***/app/\**** directory. All the docs are in seperate files for each python file and stored in ***/docs/\****


## API mapping

The API mapping to the program features / functions is tabulated and described in _Table 1_ of the PDF document ***/CURL and API mapping/CURL Communication and API map.pdf***. 


## CURL commands

The use of CURL commands and how they are communicate with the API backend is described in _Table 2_ of PDF document ***/CURL and API mapping/CURL Communication and API map.pdf***. The enumerated listin in _Table 1_ and _Table 2_ correlates. This means, row 1 in in _Table 1_ corresponds to the CURL countepart in _Table 2_.




# 3. Running tests

The Unit tests are writen using the Django Rest Framework APITestCase. These test's __doc__ strings provide information on what requirement per the supplied project definition document (PDD) the test case is testing. The test function names are also self explanatory. Furthermore, the ***/docs/app.test.html***  can be used to find the test case infromation. Comments are embedded in the code for further clarity.

To perform a test run, open two terminals both in the project root (where the manage.py file resides).
First start the server issuing this command in _Terminal 1_:

```
python manage.py runserver 8000
```

then run the following command in _Terminal 2_ to run perform a test run,

```
python manage.py test
```

The tests results will show in _Terminal 2_.




# 4. Populating DB with dummy data

In the project the script to perform a randomized data loading into the DB is a command. This file is placed in ***/app/management/commands/setup_test_data.py***. This commands uses ***/app/factories.py***
which is a class using the native python ```factory``` and ```factory.django``` packages to generate dummy data creation. The command performas 5 operations:

* Deletes all records from the database for all tables except for the superuser account in the User table.
* Creates new 5 dummy users using ```UserFactory```.
* Creates new 30 savings accounts for random existing users using ```SavingsAccountFactory```.
* Creates new 20 credit accounts for random existing users using ```CreditAccountFactory```.
* Creates new 100 transactions for random users and acccounts using```TransactionFactory```.

To run the dummy data creation and population, run the following command from the project root (where the manage.py file resides).


```
python manage.py setup_test_data
```

# 5. Admin page

The admin page was not implemented exactly per Requirement 8 in the project definition document because of time contraints. However a native django admin page was used to display the following database models

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

* Username : admin
* Password : admin



# 6. Downloading the CSV file

The CSV file per Requirement 9 in the project definition document can be downloaded by 1st running the dev_serve as shown above and then entering the download link (http://localhost:8000/csv/) in the URL field. As soon as you submit, the CSV file will download.


