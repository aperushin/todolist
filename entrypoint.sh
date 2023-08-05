#!/bin/bash
python todolist/manage.py migrate --check
status=$?
if [[ $status != 0 ]]; then
  python todolist/manage.py migrate
fi
exec "$@"
