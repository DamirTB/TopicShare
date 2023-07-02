# Flask application Forum

Web application is written in flask framework, the application itself represents a forum with basic features where users can share their thoughts through the Forum or discuss specific topics in comment sections under each topic. 

## step 1

first of all create a virtual environment 
```
py -3 -m venv env
```

## step 2

activate your virual environment 

```
env\Scripts\activate
```

## step 3

install all required packages

```
pip install -r requirements.txt
```

## step 4

Type into your terminal this command `SET FLASK_APP=app.py` then type `flask shell`. After wards a flask shell will pop out, and you need to write these commands

```
from app import app, mydb

mydb.create_all()

exit()
```

## step 5

The application is ready to use, type the following command
`flask run`