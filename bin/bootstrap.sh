#!/usr/bin/env bash

echo "deb http://apt.postgresql.org/pub/repos/apt/ wheezy-pgdg main" > /etc/apt/sources.list.d/pgdg.list

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
apt-get update
apt-get upgrade

apt-get install -y postgresql-9.4 python-pip python-dev postgresql-server-dev-9.4
pip install virtualenvwrapper

sudo -u postgres createuser --superuser vagrant
sudo -u postgres createdb slothair

cp -R -f /vagrant/etc /

/etc/init.d/postgresql restart

su vagrant
cd /home/vagrant

mkdir /home/vagrant/.envs
sudo chown -R vagrant /home/vagrant/.envs
echo "export WORKON_HOME=/home/vagrant/.envs" >> /home/vagrant/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
export WORKON_HOME=/home/vagrant/.envs
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv slothair
echo "workon slothair" >> /home/vagrant/.bashrc

cd /vagrant

pip install -r requirements.txt

cd /vagrant/bin
exec ./getdata.sh