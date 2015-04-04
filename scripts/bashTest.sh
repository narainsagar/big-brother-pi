#!/bin/bash
#generate keys
#ssh into raspberry
#copy python source files

echo '***************start changing directory permissions'
sudo chmod 777 /var/www/
echo '***************Done changing /var/www/ rights to 777'


echo '***************start making new directory big-brother-pi'
mkdir /var/www/big-brother-pi
echo '***************Done creating new directory in /var/www/ as big-brother-pi' 


echo '***************start coping python and bash files in /var/www/big-brother-pi'
cd /var/www/big-brother-pi
git clone https://talib_570@bitbucket.org/mashhoodr/big-brother-pi.git
echo '***************Done coping files'

echo '***************start changing directory permissions'
sudo chmod 644 /var/www/
echo '***************Done changing /var/www/ rights to 777'

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
sudo easy_install pycurl
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

echo '***************start change directory'
cd /var/www/big-brother-pi/
echo '***************Done change directory'

#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "*/15 * * * * python main.py" >> mycron
echo "01 */1 * * * python ping.py" >> mycron
echo "@reboot python launcher.py" >> mycron
#install new cron file
crontab mycron
rm mycron

echo "bye bye world"