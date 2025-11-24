#!/bin/sh
rm /start.sh

echo ${GZCTF_FLAG} > /flag
chown root:root /flag
chmod 400 /flag
unset GZCTF_FLAG

cd /app

exec bython app.by