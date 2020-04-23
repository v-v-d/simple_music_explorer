#!/bin/sh
set -e

/bin/sh /opt/code/db/start_postgres.sh

echo 'Creating Schema'
python3 /opt/code/init_db.py

/bin/sh /opt/code/db/stop_postgres.sh
