#!/bin/bash
set -e

if [ "$AUTO_APPLY_MIGRATIONS" = 1 ]; then
  yoyo apply --database mysql://"$DB_LOGIN":"$DB_PASSWORD"@"$DB_SERVER"/"$DB_NAME"
fi

exec python3 service.py
