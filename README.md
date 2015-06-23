The purpose of this script is to notify current active nodes inside a network periodically. 
It uses fing command line tool for the network discovery.
We deployed this script on raspberry pi which was connected with our router for tracking in-house attendance.

Dependencies
    libcurl
    pycurl
    fing
    sqlite3

Installing dependencies on raspberry pi:
    sqlite3:
        sudo apt-get install sqlite3
    
    libcurl:
        sudo apt-get install -y libcurl4-openssl-dev
        sudo apt-get install -y libcurl4-gnutls-dev librtmp-dev
    
    pycurl:
        sudo apt-get install python-pycurl
    
    fing:
        wget http://www.overlooksoft.com/packages/download?plat=arm
        mv download\?plat\=arm overlook-fing.deb
        sudo dpkg -i overlook-fing.deb
    
    
Setting up the script:
    transfer all the files to raspberry pi
    set an environment variable COMPANY_ID with some random string
    set the urls for the script to send the data to
    set up cron jobs to execute main.py and log.py at fixed intervals
    
    
To automate the whole process, there is a bash script DeployementReady.sh. On execution, 
    it will ask for a company id and automatically and set the environment variable
    download the latest version of the script from this repo
    install all the dependencies
    set up cron jobs to be executed at a fixed interval
    
    

