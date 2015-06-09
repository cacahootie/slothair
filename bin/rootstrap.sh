#!/usr/bin/env bash

echo "deb http://apt.postgresql.org/pub/repos/apt/ wheezy-pgdg main" > /etc/apt/sources.list.d/pgdg.list

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
apt-get update
apt-get upgrade

apt-get install -y postgresql-9.4 python-pip python-dev postgresql-server-dev-9.4
pip install virtualenvwrapper

sudo -u postgres createuser --superuser slothair
sudo -u postgres createdb slothair

cp -R -f /opt/slothair/etc /

/etc/init.d/postgresql restart
