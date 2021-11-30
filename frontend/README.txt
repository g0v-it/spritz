This is the webapp directory.
The purpose of this webapp is to collect votes, and give result of an election.
The code is based on Flask web framework.

Subdirectories:
    - static: contains images, js and all static files
    - templates: contains html files for Flask template system.
    - translations: contains translation files for Babel internationalization system.

There is not a strict distiction between frontend and backend, because everything is in the same directory.
We used a strict separation of roles of code, explaination follows.
The main file is index.py. it is a Flask main file. Every webpage is a function in this file.
It means that every function calls modules, retrieve data, put data in a template end return the webpage.
We have few types of modules:
    * DAO modules: objects and function accessing DB
    * BO modules: objects and function implementing business logic.
    * test modules: test classes for BO and DAO mobules
    * model.py: map objects to DB tables in database using SqlAlchemy. Every object has comments explaining his purpose.
    * config.py: retrieve configuration from environment

To setup and run system in your pc you need following:
  - install postgresql
  - create the database in database/postgresql/create.sql
  - configure environment variables (see config.py)
  - set SPRITZ_AUTH as 'test'
  - install python modules (see requirements.txt)
  - run index.py
  - point your browser to http://localhost:5000/
  - login as 'aldo' with password 'aldo'

Virtualenv is highly recommended.
If you use Visual Studio Code or another dev editor, you can set environment variables in the editor configuration.


