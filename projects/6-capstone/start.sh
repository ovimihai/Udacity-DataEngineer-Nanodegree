#!/bin/sh


export NB_UID=$(id -u)
export NB_GID=$(id -g)

echo "${NB_UID}:${NB_GID}"

# docker-compose down

docker-compose up -d

