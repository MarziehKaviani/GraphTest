# Graph Backend Project

This is a python django project, which has some written parts. You should complete the project by doing the following steps (Using git counts as an advantege):

1. Add two models to store `Movies` and `Artists`. Also store the `director` of the movie as a `one to many` relation between artists and movies, and `actors` as a `many to many` relation of the models.
2. Provide needed APIs to create, list, edit and delete a movie. Also provide APIs to create, list, edit and delete an artist. Also implement a filtering to filter directors and actors via appropriate query param.
2. Complete the `Postgresql extension view` to retrieve all `installed extension` on the database.
3. Design a view to store and retrieve each `endpoint` and it's `Call Count`. Also add an api to retrieve this data.


## Project Structure

### Database:
This project uses postgresql `docker`. To run and connect to the database, simply go to database folder and start the docker compose using:
```
cd database/
```
If your system uses the newer versions of docker, use:
```
docker compose up 
```
otherwise:
```
docker-compose up
```


### Python, Django Backend
For the main `django` part, we use a combination on python `virtual environment` and python code itself. The virtual environment and it's needed packages are provided. So if you want to run the project simply activate the virtual environment and run server.
First create a virtual environment and then install the packages:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver (or do other commands like migrate, makemigrations and etc.)
```

### API Call and testing

It is recommended to use a tool like `postman` to document and test your APIs. It will be appreciated to export the api documentation and put it into the project.
# GraphTest
