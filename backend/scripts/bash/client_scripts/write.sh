#!/bin/bash

# Create short URL through nginx
curl -X POST "http://localhost/api/write/urls" \
     -H "Content-Type: application/json" \
     -d '{"original_url": "https://www.ycombinator.com", "user_id": 3}'


