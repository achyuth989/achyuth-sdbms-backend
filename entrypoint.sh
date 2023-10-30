#!/bin/sh

cd /roboxa-sdbms-backend
pip3 install -r requirements.txt

python create_tables.py

# python3 manage.py migrate

exec "$@"
