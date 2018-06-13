#!/bin/bash
export FLASK_ENV=development
rm -rf data migrations
flask create_db
flask db init
flask db migrate
flask run -h 0.0.0.0 -p 8877
