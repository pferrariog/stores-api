#!/bin/sh

poetry run flask db upgrade

exec poetry run gunicorn -b 0.0.0.0:80 "stores.app:create_app()"
