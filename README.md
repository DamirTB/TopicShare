# Overview

TopicShare is a web application developed using the Flask framework. It serves as a forum platform with essential features, allowing users to share their thoughts and engage in discussions on various topics. Each topic has a dedicated comment section where users can participate in conversations. Additionally, TopicShare provides an administrative interface that offers comprehensive insights into user registrations, posted content, and other relevant website information.

## These tools are used in the development process
  - Flask
  - Bootstrap
  - postgresql
  - Docker

## Setting up application
  1. First of all clone a repository by typing this command in GitBash `git clone https://github.com/DamirTB/TopicShare.git`
  2. Configure your postgresql database URI:
   ```
   app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://username:password@localhost/your_db_name" 
   ```
   or you could just use sqlite by default
   ```
   app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
   ```
  3. Create an image 
  ```
    docker build . -t flask
  ```
  4. Then create a container of that image and run it 
  ```
    docker run -p 3000:80 flask
  ```
## Documentations
 - [Documentation Flask link](https://flask.palletsprojects.com/en/2.3.x/)
 - [Documentation Bootstrap link](https://getbootstrap.com/)
 - [Documnetation Postgresql link](https://www.postgresql.org/docs/current/index.html)
 - [Demo how it work with docker](https://www.youtube.com/watch?v=cXTDihdDQug&t=15s)