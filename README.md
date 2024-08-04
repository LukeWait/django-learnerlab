# Django Learner Lab
## Description
A tutorial for Django beginners to get a project up and running. Aids in understanding the fundamentals of web framework and how they interact with databases and APIs.

**Work In Progress**
**Update**
- sql_ex project is completed with ORM, REST framework, front end view, API views/endpoints, and extensive commenting to explain the purpose of files, settings, methods, etc. I'll add the code to generate Swagger API documentation and it should be 100%.
- I'll focus on completing the nosql_ex project next, before moving my attention to the tutorial documents which are still in a rough draft state while I figure out what to cover, and in what order.

<p align="center">
  <img src="https://github.com/LukeWait/django-learnerlab/raw/main/docs/screenshots/django-learnerlab-titlepage.png" alt="Labs Screenshot" width="700">
</p>

### Features
2 Written Documents:
- Django Learner Lab Part 1 - Fundamentals of web development frameworks and associated tools
  - web dev frameworks, mvcs, and the requirements of modern web dev design
  - front/back end options and how they fit in with framework/mvc
  - use of IDE and git for modern development
  - Django project contents, use of vm, servers, containers, and ci/cd pipelines for deployment
  - apis, endpoints, and the need for testing and documentation
  - intro the Part 2 practical activities and additional learning resources
- Django Learner Lab Part 2 - Getting started with remote access, backend data modeling, and API endpoints
  - setting up a virtual machine to host django projects and allow remote access
  - cloning repo to vm and setting up the environments via IDE on host machine
  - exploring the sql_ex django project to understand framework structure and ORM functionality
  - exploring the nosql_ex django project, including connecting to external db and creating/testing api endpoints
  - generating api documentation with swagger
  - starting a new project, command cheat sheets, and further learning avenues

2 Django Projects:
These will facilitate the means to complete the practical labs outlined in Django Learner Lab Part 2.
- sql_ex
  - provides a platform to discover benefits of ORM and use of relational dbs with Django
- nosql_ex
  - highlights connections to external dbs
  - focuses on implementing api endpoints which are required for db queries

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [Testing](#testing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Source Code](#source-code)
- [Dependencies](#dependencies)

## Installation
### 1. Install Python
Ensure Python is installed on your machine:
- Linux: Python is usually pre-installed. Verify by running python3 --version.
- Mac: Python is usually pre-installed. Verify by running python3 --version.
- Windows: Download and install the latest version from the official website.

### 2. Clone the Project Repository
Clone your project repository or transfer the project files to your machine.
**All platforms:**
```sh
git clone https://github.com/LukeWait/django-learnerlab.git
cd django-learnerlab
```

### 3. Create and Activate a Virtual Environment
**Linux/Mac:**
```sh
python3 -m venv djangolab_venv
source djangolab_venv/bin/activate
```

**Windows:**
```sh
python -m venv djangolab_venv
djangolab_venv\Scripts\activate.bat
```

### 4. Install Project Dependencies
Install the required packages using `requirements.txt`:
**All platforms:**
```sh
pip install -r requirements.txt
```

### 5. Run Database Migrations
Apply the migrations to set up your database schema and run the server if testing/managing through browser.
**All platforms:**
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Usage
powerpoints - links
what to expect/takeaways

## Development
This project provides basic project templates/boilerplate code.

## Testing
No

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
Peter Darcy
David Hunt

## Source Code
The source code for this project can be found in the GitHub repository: [https://github.com/LukeWait/django-learnerlab](https://www.github.com/LukeWait/django-learnerlab).

## Dependencies
