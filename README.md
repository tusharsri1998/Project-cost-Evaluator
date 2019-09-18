# Project-cost-Evaluator
Application to calculate cost of a project on the basis of work details submitted by the employees everyday


This project titled 'Project cost evaluator' uses Django Framework. The priority requirement of the project is to install latest version of Python from python.org, django can be installed using requirements.txt file.
Another way is to pip install django using command line.
Before running the project, you need to first install django and then activate virtual environment.

Command to activate virtual environment - env\scripts\activate

The environment contains most of the dependencies of the project. To activate the environment, go inside project folder using cmd, there are two folders env and estimate.
Type the command env\scripts\activate(for windows, check for other OS).
Once activated, go inside estimate folder. Then type the command, 'python manage.py runserver'.If everything is done correctly development will start on localhost:8000.

In order to access the database you need to first create a super user . command - python manage.py createsuperuser

***If you go through the code of the app there is a python file settings.py, before starting the development it is imperative to update the location of database file inside the settings.py to the location of db.sqlite3 inside the estimate folder.
