# P.O Monitoring, Scheduling and Tracking System

A full-stack Django web application built to provide an efficient system for tracking, managing, scheduling and monitoring project costing for purchase orders.

## Features

-Create, view, update, and delete Purchase Orders, Customers, and Manpower records.

-Schedule and manage itineraries per Purchase Order, with access to project costing details.

-Interactive dashboard to monitor Purchase Order statuses, with built-in search and filtering.

-Secure user authentication via login page; account registration is restricted to the Django Admin.

-Export reports to Excel for easy downloading and offline review.

-Built-in password change functionality for authenticated users.

## Prerequisites

Before you begin, ensure you have the following installed:

-Python 3.10 or higher (Required for Django 5.x compatibility)

-pip (Python package installer)

-virtualenv (recommended for isolated environments)

-Git

-PostgreSQL 12 or higher

-pgAdmin (optional, for database management)

## Installation

Follow these steps to set up the project locally:

### 1. Clone the repository
```bash
git clone https://github.com/aarown00/pom.git
cd <folder-name> or open root folder
```

### 2. Create a virtual environment
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. PostgreSQL (Local) Configuration Example
```bash
For local development using PostgreSQL, update the `DATABASES` setting in  
`mabuhaypowers_pom/settings.py` as shown below:

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mabuhaypowers_pom",
        "USER": "postgres",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```
### 5. Run database migrations
```bash
python manage.py migrate
```

### 6. Create a superuser 
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 8. Run the development server
```bash
python manage.py runserver
```

### 9. OR Run the production server
```bash
waitress-serve --host=0.0.0.0 --port=80 mabuhaypowers_pom.wsgi:application
```

The application will be available at `http://localhost:8000`

## Usage

- Access the admin panel at `http://localhost:8000/admin`

