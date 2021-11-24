
## REST API to create, manage, and share color palettes

## Requirements

- Python 3.6
- Django 3.1
- Django REST Framework

## Installation
After you cloned the repository, you want to create a virtual environment, so you have a clean python installation.
You can do this by running the command
```
virtualenv venv --python=python3
```

After this, it is necessary to activate the virtual environment, you can get more information about this [here](https://docs.python.org/3/tutorial/venv.html)

You can install all the required dependencies by running
```
pip install -r requirements.txt
```
Run migrations
```
python manage.py migrate
```
Ready to run the server.
```
python manage.py runserver
```