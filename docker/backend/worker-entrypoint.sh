#!/bin/sh

until cd /app/codeforces_app
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A codeforces_app worker --loglevel=info --concurrency 1 -E
