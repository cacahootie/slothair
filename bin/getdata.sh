#!/usr/bin/env bash

wget --quiet -O ../import/airports.dat "https://sourceforge.net/p/openflights/code/HEAD/tree/openflights/data/airports.dat?format=raw"
wget --quiet -O ../import/airlines.dat "https://sourceforge.net/p/openflights/code/HEAD/tree/openflights/data/airlines.dat?format=raw"
wget --quiet -O ../import/routes.dat "https://sourceforge.net/p/openflights/code/HEAD/tree/openflights/data/routes.dat?format=raw"