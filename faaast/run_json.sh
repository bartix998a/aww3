#!/bin/bash
curl -X 'POST' \
  'http://localhost:8000/images/del' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d @data.json