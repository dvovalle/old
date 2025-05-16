#!/bin/bash
export FLASK_DEBUG=true
export FLASK_APP=run_ssl.py
export FLASK_APP_DEBUG="true"
export PRODUCTION="false"
export FLASK_ENV=development
export ELK_ACTIVE='true'
export REDIS_ACTIVE="true"
export SQL_READONLY="false"
export WSGI_WORKERS="2"
export WSGI_THREADS="8"
export MAIL_ENABLED=true
export TESTING=False
export PROPAGATE_EXCEPTIONS=true
export SECRET_KEY='FF2B76B2-6C43-44CB-95BA-7979D49F7123'

export TZ=America/Sao_Paulo
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8
export LC_COLLATE=C
export LC_TIME=en_US.UTF-8
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1


rm -rf requirements_dev.txt

pip install --upgrade pip

for i in $(pip list -o | awk 'NR > 2 {print $1}')
do
    pip install -U $i
done

pip freeze -r requirements.txt -l > requirements_dev.txt
