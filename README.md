# litrevu

The litrevu Project is a Django-based web application that allows users to create and manage posts (tickets) and reviews. It provides a platform for users to publish posts and share their opinions by writing reviews.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [PEP8 Code compliance Report](#pep8-code-compliance-report )
	

## Features

- User authentication and registration
- Posts creation and management
- Review creation and association with tickets
- User profile management
- Following and unfollowing other users
- Activity feed displaying posts and reviews from followed users

## Prerequisites

Before you begin, please make sure that you have met the following requirements:

- Python 3.6.5 installed
- Django installed 
- Virtual environment 

***

## Installation

open your terminal use the following command:

### - Clone the project    
    'git clone https://github.com/Toufik-CHAARI/litrevu.git'  

### - Change directory    
    'cd litrevu'

### - Create virtual env     
   'python3 -m venv venv'

### - Activate virtual environment
   'source venv/bin/activate'

### - Install django
    'pip install django'

### - Install the dependencies 
    'pip install -r requirements.txt'

### - Make the migrations    
    'python manage.py migrate'

### - Create admin super user
   'python manage.py createsuperuser'

### - Run the web application locally 
    'python manage.py runserver'

***

## PEP8 Code compliance Report

## In order to generate each report, please use the following commands :

### flake8 --format=html --htmldir=flake-report_articles articles/admin.py
### flake8 --format=html --htmldir=flake-report_forms articles/forms.py 
### flake8 --format=html --htmldir=flake-report_models articles/models.py
### flake8 --format=html --htmldir=flake-report_views articles/views.py
### flake8 --format=html --htmldir=flake-report_authentication_admin authentication/admin.py
### flake8 --format=html --htmldir=flake-report_authentication_forms authentication/forms.py
### flake8 --format=html --htmldir=flake-report_authentication_models authentication/models.py
### flake8 --format=html --htmldir=flake-report_authentication_views authentication/views.py

### display the reports via the index.html file within each flake-report folders