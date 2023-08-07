#!/bin/bash
python /code/todolist/manage.py migrate --check
status=$?
if [[ $status != 0 ]]; then
  python /code/todolist/manage.py migrate
fi
exec "$@"
