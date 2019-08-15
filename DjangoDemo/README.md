# Django

## Install virtual environment & build a new django project
    python3 -m venv my_env
    source my_env/bin/activate
    cd my_env
    pip install django
    pip freeze
    django-admin startproject my_proj
    python3 manage.py migrate
    python3 manage.py runserver
