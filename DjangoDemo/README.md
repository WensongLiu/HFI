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

## How to set variables in a template
    {% extends "base_generic.html" %}

    {% block title %}{{ section.title }}{% endblock %}

    {% block content %}
    <h1>{{ section.title }}</h1>

    {% for story in story_list %}
    <h2>
      <a href="{{ story.get_absolute_url }}">
        {{ story.headline|upper }}
      </a>
    </h2>
    <p>{{ story.tease|truncatewords:"100" }}</p>
    {% endfor %}
    {% endblock %}
