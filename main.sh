#!/bin/bash

#this file copy big-brother-pi to /var/www/ of raspberry pi

curl -L https://raw.githubusercontent.com/beautifulcode/ssh-copy-id-for-OSX/master/install.sh | sh

ssh-copy-id -i ~/.ssh/id_rsa.pub pi@192.168.0.111

scp ~/Sites/big-brother-pi/*.* pi@192.168.0.111:/home/pi/Downloads/

ssh pi@192.168.0.111 'bash -s' < bashTest.sh
