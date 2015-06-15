appdir="/opt/slothair"
if [ -d "/vagrant" ]; then
	appdir="/vagrant"
fi

cd ~

mkdir ~/.envs
echo "export WORKON_HOME=/home/vagrant/.envs" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
echo "workon slothair" >> ~/.bashrc
echo "alias dbshell='psql -d slothair'" >> ~/.bashrc

export WORKON_HOME=~/.envs
source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv slothair

cd $appdir

pip install -r requirements.txt

cd $appdir/bin
./getdata.sh

cd $appdir/scripts
python load_openflights.py
