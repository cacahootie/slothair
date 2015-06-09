cd ~

mkdir ~/.envs
echo "export WORKON_HOME=/home/vagrant/.envs" >> /home/web/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/web/.bashrc
echo "workon slothair" >> /home/web/.bashrc
echo "alias dbshell='psql -d slothair'" >> /home/web/.bashrc

export WORKON_HOME=/home/web/.envs
source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv slothair

cd /opt/slothair

pip install -r requirements.txt

cd /opt/slothair/bin
./getdata.sh

cd /opt/slothair/scripts
python load_openflights.py
