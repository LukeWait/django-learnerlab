# Django Learner Lab
## Description
A tutorial for Django beginners to get a project up and running. Aids in understanding the fundamentals of web framework and how they interact with databases and APIs.

### Work In Progress
**Update**
- sql_ex project is completed with ORM, REST framework, front end view, API views (ViewSets), Routers and URL patterns, OpenAPI documentation support, and extensive commenting to explain the purpose of files, settings, methods, etc.
- nosql_ex project has been setup with connectivity to MongoDB (PyMongo) and can retrieve documents. OpenAPI documentation working. REST framework library not utilized to highlight management of self-created views. Extensive commenting in place. Currently working on custom auth/admin app.
- Tutorial documents are taking shape. The topics that will be covered have placeholder slides at the very least and some of the tutorial sections are well on their way. 

<p align="center">
  <img src="https://github.com/LukeWait/django-learnerlab/raw/main/docs/screenshots/django-learnerlab-titlepage.png" alt="Labs Screenshot" width="700">
</p>

### Features
#### Written Material:
- **Django Learner Lab Part 1 - Fundamentals of web development frameworks and associated tools**
  - Web dev frameworks, MVCs, and the requirements of modern web dev design
  - Front/back end options and how they fit in with framework/mvc
  - Use of IDEs and git for modern development
  - Django project contents, use of vm, servers, containers, and ci/cd pipelines for deployment
  - APIs, views, endpoints, and the need for testing and documentation
  - Intro the Part 2 practical activities and additional learning resources
- **Django Learner Lab Part 2 - Getting started with remote access, backend data modeling, and API endpoints**
  - Setting up a virtual machine to host Django projects and allow remote access
  - Cloning repo to VM and setting up the environments via IDE on host machine
  - Exploring the sql_ex django project to understand rest framework structure and ORM functionality
  - Exploring the nosql_ex django project, including connecting to external NoSQL database and creating/testing api endpoints
  - Generating API documentation with Swagger/ReDoc
  - Starting a new project, command cheat sheets, and further learning avenues

#### Pre-made Django Projects:
These will facilitate the means to complete the practical labs outlined in Django Learner Lab Part 2.
- **sql_ex**
  - provides a platform to discover benefits of ORM and use of relational dbs with Django
- **nosql_ex**
  - highlights connections to external dbs and challenges of not using models/ORM

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
It is recommended to host the pre-made Django projects on a Linux virtual machine and access them via an IDE from the host machine. Details on how to achieve this is covered in Django Learner Lab Part 2 documentation.

### 1. Install Python
Ensure Python is installed on your machine:
- Linux: 
```sh
sudo apt install python3 python3-pip python3-venv
```
- Mac:
```sh
brew install python
```
- Windows: Download and install the latest version from the [official website.](https://www.python.org/downloads/)

### 2. Clone the Project Repository
Clone your project repository or transfer the project files to your machine.
**All platforms:**
```sh
git clone https://github.com/LukeWait/django-learnerlab.git
cd django-learnerlab
```

### 3. Create and Activate a Virtual Environment for Each Project
As each project has different dependencies/package requirements, it is recommended to create a separate Pthyon virtual environment for each. The following commands are for the sql_ex project. Repeat the process for the nosql_ex project. To deactivate an acitve virtual environment, simply use the command 'deactivate'.
**Linux/Mac:**
```sh
cd sql_ex
python3 -m venv sql_ex_venv
source sql_ex_venv/bin/activate
```

**Windows:**
```sh
cd sql_ex
python -m venv sql_ex_venv
sql_ex_venv\Scripts\activate.bat
```

### 4. Install Project Dependencies
Install the required packages using the supplied `requirements.txt` for each project. The command line will indicate when a virtual environment is active, for example (sql_ex_venv). Ensure you are in the directory of the correct project with the virtual environment active and use the following command:
**All platforms:**
```sh
pip install -r requirements.txt
```

You're now ready to run the Django server and proceed with the Learner Labs! Please refer to the Django Learner Lab Part 2 document for further details.

## Usage
1. Clone the repo to your host machine and access the Django Learner Lab docs:
    - Django Learner Lab Part 1 - Fundamentals of web development frameworks and associated tools
    - Django Learner Lab Part 2 - Getting started with remote access, backend data modeling, and API endpoints
2. Clone the repo to a machine to act as the Django server (recommended to use a separate machine to the host, such as a virtual machine running Ubuntu Linux).
3. Access the Django server via SSH.
4. Follow the Django Learner Lab Part 2 document for comprehensive tutorial on how to navigate the pre-made Django projects and start a new project.

## Development
The Django projects contained in this repo contain project templates/boilerplate code, as well as extensive commenting to provide a deeper understanding of the files and purpose of the code being used. The projects could be used as a starting point to build from, however, the Django Learner Lab Part 2 will provide all the commands and know how to create a new project from scratch.

## Testing
**sql_ex**
- Fully functional with ORM, API, and admin portal.
- API endpoints tested succesfully with ThunderClient and Swagger.
- Authorization restrictions are in place and endpoints responding as expected.

**nosql_ex**
- Custom API views and external MongoDB connection has been established.
- API endpoints tested succesfully with ThunderClient and Swagger.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Peter Darcy
- David Hunt

## Source Code
The source code for this project can be found in the GitHub repository: [https://github.com/LukeWait/django-learnerlab](https://www.github.com/LukeWait/django-learnerlab).

## Dependencies
**sql_ex**
- asgiref==3.8.1
- Django==5.1.9
- djangorestframework==3.15.2
- drf-yasg==1.21.7
- inflection==0.5.1
- packaging==24.1
- PyJWT==2.9.0
- pytz==2024.1
- PyYAML==6.0.1
- sqlparse==0.5.1
- typing_extensions==4.12.2
- uritemplate==4.1.1

**nosql_ex**
- asgiref==3.8.1
- certifi==2024.7.4
- charset-normalizer==3.3.2
- Django==5.1.9
- dnspython==2.6.1
- drf-yasg==1.21.7
- idna==3.7
- inflection==0.5.1
- packaging==24.1
- pymongo==4.8.0
- pytz==2024.1
- PyYAML==6.0.2
- requests==2.32.3
- sqlparse==0.5.1
- typing_extensions==4.12.2
- uritemplate==4.1.1
- urllib3==2.2.2
