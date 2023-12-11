# Recipe Builder
An SDEV-265 Group Project

## Setup

**You will want to make sure that you already have Python installed on your system.**

Windows
---------
1. First, setup your virtual environment from the project's root folder.
> virtualenv venv

❗ pip install virtualenv if you do not have Python's virtual environment already.

2. Activate the virtual environment.
> venv\Scripts\activate

❗ Make sure to always activate the environment before working on the project.

3. Next, you'll need to install dependencies to your virtual environment.
> pip install -r requirements.txt

4. You will then want to move into the src folder.
> cd src

5. If you do not have an existing database, go ahead and:
> python manage.py makemigrations
> python manage.py migrate
> python manage.py createsuperuser

6. Register for an Edamam API Account, create a .env file in src and add your APP_ID and APP_KEY there.
> EDAMAM_APP_ID = "APP_ID_HERE"
> EDAMAM_APP_KEY = "APP_KEY_HERE"

7. You can now run the server
> python manage.py runserver

Mac
---------
1. Setup virtual environment.
> Python3 -m venv myvenv

2. Activate the virtual environment.
> source myvenv/bin/activate

❗ Make sure to always activate the environment before working on the project.

3. Next, you'll need to install dependencies to your virtual environment.
> pip install -r requirements.txt

4. If you do not have an existing database, go ahead and:
> python manage.py makemigrations
> python manage.py migrate
> python manage.py createsuperuser

5. Register for an Edamam API Account, create a .env file in src and add your APP_ID and APP_KEY there.
> EDAMAM_APP_ID = "APP_ID_HERE"
> EDAMAM_APP_KEY = "APP_KEY_HERE"

6. You can now run the server.
> python src/manage.py runserver
