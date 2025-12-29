#!/bin/bash

until curl -s http://app:8080; do
  sleep 1
done


curl -X 'POST' \
        'http://127.0.0.1:8080/api/roles/' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "role_name": "Администратор"
    }'

curl -X 'POST' \
        'http://127.0.0.1:8080/api/roles/' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "role_name": "Пользователь"
    }'
