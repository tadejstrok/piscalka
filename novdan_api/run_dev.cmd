@echo off
set DJANGO_DATABASE_HOST=localhost
set DJANGO_DATABASE_NAME=novdanapi
set DJANGO_DATABASE_USERNAME=novdanapi
set DJANGO_DATABASE_PASSWORD=novdanapi
set DJANGO_RUNSERVER_HIDE_WARNING=true
"%~dp0venv\Scripts\python.exe" "%~dp0manage.py" runserver 0.0.0.0:8000
