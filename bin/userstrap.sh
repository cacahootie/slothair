cd ~

mkdir ~/.envs
echo "export WORKON_HOME=/home/vagrant/.envs" >> /home/vagrant/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
echo "workon slothair" >> /home/vagrant/.bashrc
echo "alias dbshell='psql -d slothair'" >> /home/vagrant/.bashrc

export WORKON_HOME=/home/vagrant/.envs
source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv slothair

cd /vagrant

pip install -r requirements.txt

cd /vagrant/bin
./getdata.sh

cd /vagrant/scripts
python load_openflights.py
