#!/usr/bin/env bash
set -e
py.test --cov-report term-missing --cov=service --mysql_database=faf-league -o testpaths=tests "$@"
