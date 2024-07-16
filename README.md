# Blog API Project

This is a simple Blog API in python with unit test

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
1. create a file named .env
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
