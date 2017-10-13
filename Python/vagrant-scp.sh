#!/bin/bash
PORT=2222
if [ ${VAGPORT} ]; then
  PORT=${VAGPORT}
fi
VAGRANT_GEM=$(dirname `gem which vagrant`)/..
VAGRANT_KEY=${VAGRANT_GEM}/keys/vagrant
chmod 600 ${VAGRANT_KEY}
ssh -i ${VAGRANT_KEY} -p ${PORT} vagrant@vagrant-ubuntu-trusty-64

#need to test this:
#OPTIONS=`vagrant ssh-config | awk -v ORS=' ' '{print "-o " $1 "=" $2}'`;
#ssh ${OPTIONS} localhost