# slothair
Flight Route Viewer

Installation Instructions
==========================

Do your git clone, cd into the directory, then:

	vagrant up && vagrant ssh
	cd /vagrant
	python run.py

All of the data will be downloaded, converted and loaded into the Postgres DB
that is installed, also part of the process.  This Vagrant setup should only
be used for development purposes because the Postgres setup is not secure.

If you'd like to modify the Postgres 9.4 host file to suit your preferences,
edit `etc/postgresql/9.4/main/pg_hba.conf` in this repo prior to executing
`vagrant up`.  Keep in mind the db/user is slothair and it expects to log in
with no password over Unix socket in this configuration.

Data Acknowledgement
=====================

This application relies upon and during the vagrant provisioning will download
data from openflights.org.  Data is used pursuant to the Open Database License.