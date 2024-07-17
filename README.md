# Blog API Project

This is a simple Blog API in python with unit tests. This app is designed using SQLite database which
is lightweight and serverless relational database management system. Its advantages are its fast and 
easy to set up and ideal for simple projects. However, consequently its performance will be lacking if
dataset become huge and complex. Also, for security practice, the app is designed using JWT which
authenticate the user and authorize the api requests by the user. The downside of this design is that we
need to ensure that the secret key is kept secret or else the request can be compromised. Some ideas to
add on to this app may be to add a frontend user interface which can actually interact with the apis in a
meaningful way. Also, I think using a framework with oauth2.0 is the more modern way to delegate user access
to resources which may be something that can be improved and using another database like mysql if we want
to scale the system as it become more complex.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Service](#setup-service)

## Prerequisites
First install on your machine:
- Python 3.11+ https://www.python.org/downloads/
- pip 24.1.2 https://pypi.org/project/pip/
- Sqlite https://www.sqlite.org/download.html

You can then install the libraries with the following command:

```bash 
pip install <library_name>
```
Libraries to install:

- PyJWT
- SQLAlchemy
- Flask
- bcrypt
- python-dotenv

## Setup environment variable
1. create a file named .env under **src** file
2. Copy and paste the following into the file and edit the values as necessary

```bash
SECRET_KEY=ANY_SECRET_VALUE
SQLALCHEMY_DATABASE_URI=sqlite:///path_to_sqlite.exe_file_on_your_local_machine
SQLALCHEMY_TRACK_MODIFICATIONS=False
```

## Setup Service

1. Clone the repository
2. Open project with PyCharm and download missing dependencies/libraries
3. Edit the **config.py** file 
4. Run the file **run.py** in Pycharm on regular run mode to run the service

## Testing
To run the unit test to test the API service, follow the steps above and then run the **tests.py** file on debug mode.
