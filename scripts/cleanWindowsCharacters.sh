#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TABLESFULL=$DIR/../data/tables_complete/*
ATTRIBUTESFULL=$DIR/../data/attributes_complete/*

#clean from tables
for t in $TABLESFULL
do
  echo "processing $t"
  t_bak="${t##*/*/}.bak"
  fullpath="${t%/*}"
  t_bak="$fullpath/$t_bak"
  tr -d "\015" < $t > $t_bak
  mv $t_bak $t
done

#clean from attributes files
for t in $ATTRIBUTESFULL
do
  echo "processing $t"
  t_bak="${t##*/*/}.bak"
  fullpath="${t%/*}"
  t_bak="$fullpath/$t_bak"
  tr -d "\015" < $t > $t_bak
  mv $t_bak $t
done
