
# Django Project Setup

This guide will help you set up the Django project on your local machine.

## Prerequisites

- Python 3.x installed on your system.
- PostgreSQL installed and running (if you are using PostgreSQL as your database).

## Setup Instructions

### 1. Create a Virtual Environment

To create a virtual environment, navigate to your project directory and run:

```sh
python -m venv .venv
```
### 2. Activate the Virtual Environment

On Windows

```sh
.venv\Scripts\activate
```

On Linux/MacOS

```sh
source .venv/bin/activate
```

### 3. Install Requirements
Install the necessary packages by running:

```sh
pip install -r requirements.txt
```

### 4. .env Setup
 Create a .env file in root and add ``SECRET_KEY``,``ALLOWED_HOSTS``,``DB_NAME``,
``DB_USER``,
``DB_PASSWORD``,
``DB_HOST``,
``DB_PORT``.

### 5. Initialize the Database and Run Migrations

Run the following command to initialize the PostgreSQL database and apply migrations:

```sh
python manage.py init_db
```

### 6. Run the Development Server

Start the Django development server with:

```sh
python manage.py runserver
```
You can now access the project at http://127.0.0.1:8000.

### 7. Swagger Documentation

You can access the project swagger documentation at http://127.0.0.1:8000/swagger/.