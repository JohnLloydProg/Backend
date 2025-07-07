#!/usr/bin/env bash

set -o errexit

python manage.py expire_session_check

python manage.py expire_qr_check

python manage.py tally_attendance

