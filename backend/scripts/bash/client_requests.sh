#!/bin/bash

curl -X POST "http://localhost:8000/urls" \
     -H "Content-Type: application/json" \
     -d '{"original_url": "https://www.fooliobar.com", "user_id": 3}'
