### INF601 - Advanced Programming in Python
### Kody Kirk
### Mini Project 3
 
 
# Project Title
 
Mini project 3: Webpages in Flask

## Description
 
This is a webpage built using Flask and Bootstrap that I thought would be fun to build out for my tabletop gaming server to have a single place for getting files, links, etc.

## Getting Started

### Installing
 
* Download the files from this repository.

### Downloading Dependencies
 
* Package requirements are in the requirements.txt file. To install, run:
```
pip install -r requirements.txt
``` 
### Executing program

* First, initialize the SQL database by running:
```
flask --app tabletoplocal init-db
```
* Then start the webserver:
```
flask --app tabletoplocal run
```
The webpage will then be accessible at http://127.0.0.1:5000.

At the moment, a hardcoded admin account is set up when the database is initialized. Username and password are both 'admin'. Other user accounts can be created with the 'register' functionality. 

Currently, the only 'admin' functions are to add games to the game list via a button that does not appear unless you are logged in as admin.  

## Authors
 
Kody Kirk

## Version History

* 0.1
    * Initial Release
 
## Acknowledgments
 
Inspiration, code snippets, etc.
* [Flask](https://flask.palletsprojects.com/en/stable/)
* [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
* [Gemini](https://gemini.google.com/)
