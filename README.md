# twitter-clone
This is a basic Twitter clone made with Django and Python. As of now, the site provides fundamental functionalities similar to Twitter, with a simplistic UI.

Please note that the current version of the application does not include any elaborate front-end design. However, future updates may include major enhancements to improve UI & UX.

This app is not yet live. To see how this app works or looks, follow below steps:

## Prerequisites:
  * Python 3.x or later installed on your system
  * pip package manager
  * PgAdmin4 database manager tool, if you have PostgreSQL installed

## Steps to follow:

* Clone this repo in your local machine and open the directory:

   `git clone https://github.com/sandeshpd/twitter-clone.git`
  
    `cd twitter-clone`

* Open any IDE/Code Editor or even default CLI would do too & install dependencies:

  `python3 -m venv env` (you can rename `env` as you want)
  
  `source env/bin/activate` (activate virtual environment in Linux)

  `env\Scripts\activate` (activate virtual environment in Windows)

* Navigate to the project directory if you haven't already:

* Apply database migrations. If you make any changes in `models.py` file, then this command is needed to run to apply those changes to the database.

  `python3 manage.py makemigrations`

  `python3 manage.py migrate`

* Create a Superuser (optional but recommended):

  `python3 manage.py createsuperuser`
  
  * Provide necessary info Django asks.

* Run the development server:

  `python3 manage.py runserver`

* Open your browser and navigate to `http://127.0.0.1:8000/`

* That's it. You will now see the Twitter clone app made with **Django** and **Python**.

 ## Additional Notes

* Modify settings in `twitter-clone/settings.py` to suit your needs, such as database configurations, static files settings, etc.

* Ensure to set `DEBUG = False` in production settings and keep your SECRET_KEY secure.

* For production deployment, consider using WSGI servers like Gunicorn or uWSGI, and reverse proxy servers like Nginx or Apache.
