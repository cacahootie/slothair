#!/usr/bin/env bash

wget --quiet -O ../import/airports.dat "https://sourceforge.net/p/openflights/code/HEAD/tree/openflights/data/airports.dat?format=raw"
wget --quiet -O ../import/airlines.dat "https://sourceforge.net/p/openflights/code/HEAD/tree/openflights/data/airlines.dat?format=raw"
wget --quiet -O ../import/routes.dat "https://sourceforge.net/p/openflights/code/HEAD/tree/openflights/data/routes.dat?format=raw"

iconv -c -f ISO8859-1 -t ASCII ../import/airlines.dat > ../import/airlines.csv
iconv -c -f ISO8859-1 -t ASCII ../import/airports.dat > ../import/airports.csv
iconv -c -f ISO8859-1 -t ASCII ../import/routes.dat > ../import/routes.csv

rm ../import/airlines.dat
rm ../import/airports.dat
rm ../import/routes.dat