#!/bin/bash

set -exo pipefail
cd -P -- "$(dirname -- "$0")"
script_path=$(pwd -P)

. .venv/bin/activate

STARTED=$(date)
./dl_all.py
./extract_table.py
./plot.py
./stochastics.py
sleep 2  # Force a new timestamp, even if running tightly for some reason
./write_html.py

cd target
git add -u
git commit -m "Automatic update $(date)

Started ${STARTED}"
# git push
