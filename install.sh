#! /bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

sudo mkdir -p /opt/audiblex
sudo cp . /opt/audiblex -rp
sudo mv /opt/audiblex/audiblex.py /opt/audiblex/audiblex
sudo ln -sf /opt/audiblex/audiblex /usr/bin/audiblex