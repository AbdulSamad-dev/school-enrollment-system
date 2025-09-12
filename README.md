username: admin
password: admin


# Guide: Cloning and Running Django Project (without virtual environment)

## 1. Clone the Repository
Open your terminal/command prompt and run:
    git clone https://github.com/AbdulSamad-dev/school-enrollment-system.git

This will create a folder named `school-enrollment-system` in your current directory.

## 2. Navigate into the Project Folder
    cd school-enrollment-system

## 3. Install Requirements
Since you are not using a virtual environment, packages will be installed globally.
Make sure you have `pip` installed and then run:
    pip install -r requirements.txt

(If requirements.txt is missing or incomplete, you may need to install manually: 
    pip install django
    pip install reportlab
    pip install pillow
and any other packages used in the project.)

## 4. Database Setup
If the repository contains `db.sqlite3`, the database with data is already included.
Otherwise, create a new database by running migrations:
    python manage.py migrate

## 5. Create Superuser (Optional, for admin login)
    python manage.py createsuperuser

Follow the prompts to set username, email, and password.

## 6. Run the Development Server
    python manage.py runserver

Open your browser and go to:
    http://127.0.0.1:8000/

You should now see the project running.

## 7. Troubleshooting
- If you get "Module not found" errors, install the missing package with pip.
- If you get database errors, remove `db.sqlite3` (if no data needed) and run `python manage.py migrate` again.
- If static files don’t load, run:
    python manage.py collectstatic

----------------------------------------------------
This guide assumes:
- You have Python 3.x installed and available in PATH.
- You are not using a virtual environment (so global site-packages will be used).
