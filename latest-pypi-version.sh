#!/bin/bash

if [ "$1" == "" ]; then
  echo "usage: $0 <package name>"
  exit 1
fi

PACKAGE=$1

# get package json file with metadata
JSON=`wget -qO - https://pypi.org/pypi/$PACKAGE/json | cat | tr "," "\n"`

for J in $JSON; do
  ISVER=`echo $J | grep "\"version\""`
  if [ "$ISVER" != "" ]; then
    VER=`echo $J | cut -d : -f 2`
    VER=${VER//\"/}
    VER=${VER//\"/}
    if [ "$VER" == "source" ]; then
      continue
    fi
    if [ "$VER" == "version" ]; then
      continue
    fi
    echo $VER
    break
  fi
done

