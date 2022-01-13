#!/bin/bash

rm -rf gigtaxapi/migrations
rm db.sqlite3
python manage.py makemigrations gigtaxapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata musicians
python manage.py loaddata categories
python manage.py loaddata gigs
python manage.py loaddata tours
python manage.py loaddata receipts