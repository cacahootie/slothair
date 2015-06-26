#!/usr/bin/env bash

wget -O ../import/airports.dat "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
wget -O ../import/airlines.dat "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat"
wget -O ../import/routes.dat "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat"

iconv -c -f ISO8859-1 -t ASCII ../import/airlines.dat > ../import/airlines.csv
iconv -c -f ISO8859-1 -t ASCII ../import/airports.dat > ../import/airports.csv
iconv -c -f ISO8859-1 -t ASCII ../import/routes.dat > ../import/routes.csv

rm ../import/airlines.dat
rm ../import/airports.dat
rm ../import/routes.dat