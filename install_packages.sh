#!/bin/sh

for EACH in flask flask-login flask-admin flask-sqlalchemy sqlalchemy requests;
do
    sudo pip install $EACH
done
