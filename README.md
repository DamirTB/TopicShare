# Overview

TopicShare is a web application developed using the Flask framework. It serves as a forum platform with essential features, allowing users to share their thoughts and engage in discussions on various topics. Each topic has a dedicated comment section where users can participate in conversations. Additionally, TopicShare provides an administrative interface that offers comprehensive insights into user registrations, posted content, and other relevant website information.

## These tools are used in the development process
  - Flask
  - Bootstrap
  - postgresql

## Setting up application
  1. create a virtual environment `py -3 -m venv env`
  2. activate your virtual environment `env\Scripts\activate`
  3. install all required packages `pip install -r requirements.txt`
  4. Type into your terminal this command `SET FLASK_APP=app.py` then type `flask shell`. Afterwards a flask shell will pop out, and you need to write these commands
  ```
  from app import app, mydb

  mydb.create_all()

  exit()
  ```
  5. Congratulations! The web application is ready to use, all you have to do is type `flask run` to launch

## Documentations
 - [Documentation Flask link](https://flask.palletsprojects.com/en/2.3.x/)
 - [Documentation Bootstrap link](https://getbootstrap.com/)
 - [Documnetation Postgresql link](https://www.postgresql.org/docs/current/index.html)