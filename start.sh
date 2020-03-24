#!/bin/bash

ROOTPATH=$(cd $(dirname $0); pwd -P)

source $ROOTPATH/venv/bin/activate
python $ROOTPATH/logkit/manage.py runserver 0.0.0.0:8081 &

