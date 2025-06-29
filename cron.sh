#!/usr/bin/env bash

set -o errexit

python manage.py dbbackup

python manage.py expire_session_check

python manage.py expire_qr_check

