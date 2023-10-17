# Django Bookmark Manager

Django Bookmark Manager is a simple web application that allows you to manage your bookmarks. It provides CRUD (Create, Read, Update, Delete) operations for your bookmarks, dynamic search functionality, user registration and authorization, and the ability to assign tags to your bookmarks.

## Features

- User Registration and Authorization: Users can create accounts and log in to manage their bookmarks.
- CRUD Operations: Users can perform Create, Read, Update, and Delete operations on their bookmarks.
- Dynamic Search: Search for bookmarks based on titles, tags, url, description.
- Tagging System: Categorize your bookmarks by assigning tags to them.

## Installation

1. Clone the repository to your local machine:
```
$ git clone https://github.com/PetroFedun/bookmarks.git
$ cd bookmarks
```
2. Create a virtual environment and activate it:
```
$ python -m venv venv
$ source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
```
3. Install the project dependencies from the requirements.txt file:
```
$ pip install -r requirements.txt
```
4. Apply the database migrations:
```
$ python manage.py migrate
```
5. Run server:
```
$ python manage.py runserver
```
6. Access the application in your web browser at http://localhost:8000/manager.
