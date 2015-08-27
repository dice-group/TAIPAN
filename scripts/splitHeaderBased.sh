#!/bin/bash

TABLES=/home/ivan/datahdd/tables/*

for table in $TABLES
do
    cat $table | grep "\"hasHeader\":true" > $table-with-headers.json
    cat $table | grep "\"hasHeader\":false" > $table-no-headers.json
    rm $table
done
