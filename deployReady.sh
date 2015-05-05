#!/bin/bash
#generate keys
#ssh into raspberry
#copy python source files


# ssh pi@192.168.0.35
# touch ~/.bash_profile

# echo "please enter the company ID"
# read -r companyID

# echo "Setting Environment Variable COMPANY_ID"
# export COMPANY_ID=$companyID >> ~/.bash_profile
# echo "COMPANY_ID Set"
# exit
# ssh pi@192.168.0.35

echo '***************Started copying files'
git clone https://Suleman-ML@bitbucket.org/mashhoodr/big-brother-pi.git
echo '***************Done coping files'

echo '***************Start updating apt-get'
sudo apt-get update
echo '***************Done Update'

echo '***************start installing sqlite3'
sudo apt-get install sqlite3
echo '***************Done sqlite3'

echo '***************start installing git'
sudo apt-get install git
echo '***************Done git'

echo '***************start installing libcurl4-openssl-dev'
sudo apt-get install -y libcurl4-openssl-dev
echo '***************Done libcurl4-openssl-dev'

echo '***************start installing libcurl4-gnutls-dev librtmp-dev'
sudo apt-get install -y libcurl4-gnutls-dev librtmp-dev
echo '***************Done libcurl4-gnetls-dev librtmp-dev'

echo '***************start installing pycurl'
sudo apt-get install python-pycurl
echo '***************Done pycurl'

echo '***************start downloading fing module'
wget http://www.overlooksoft.com/packages/download?plat=arm
echo ' **************Done DOwnload deb'

echo '***************start installing expect'
mv download\?plat\=arm overlook-fing.deb
echo '***************Done rename'

echo '***************start installing expect'
sudo dpkg -i overlook-fing.deb
echo '***************Done install package'

echo '***************start installing libpCap'
sudo apt-get install libpcap*
echo '***************libpCap'

#5528ae5222335a110061b4d3

#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "*/15 * * * * . ~/.bash_profile; python ~/big-brother-pi/main.py" >> mycron
echo "01 */1 * * * python ~/big-brother-pi/ping.py" >> mycron
#install new cron file
crontab mycron
rm mycron

echo "bye bye world"