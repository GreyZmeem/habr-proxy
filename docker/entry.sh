#!/usr/bin/env sh

set -o errexit
set -o nounset

if [[ "${1#-}" != "$1" ]] || [[ "${1%.conf}" != "$1" ]]; then
	set -- pipenv run ./main.py "$@"
fi

exec "$@"
