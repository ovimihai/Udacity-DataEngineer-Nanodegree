#!/bin/sh


cd data

rm -fr input

mkdir -p input/log_data/2018/11

# sudo apt-get install unzip
unzip song-data.zip -d input
unzip log-data.zip -d input/log_data/2018/11
