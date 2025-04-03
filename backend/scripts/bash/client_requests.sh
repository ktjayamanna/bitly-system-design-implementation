#!/bin/bash

curl -X POST "http://localhost:8000/urls" \
     -H "Content-Type: application/json" \
     -d '{"original_url": "https://www.example.com/some/very/long/url", "user_id": 1}'
