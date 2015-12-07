###Overview
The purpose of this script is to notify current active nodes inside a network periodically. It uses fing command line tool internally for the network discovery. We deployed this script on raspberry pi which was connected with our router for tracking in-house attendance.

###Dependencies:

    libcurl
    pycurl
    fing
    sqlite3

###Installing dependencies on raspberry pi:
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
    
    
###Setting up the script:

#####transfer all the files to raspberry pi:

    clone the repo or either download the zip from the github
    
    from the terminal, use scp command to copy the files to the raspberry. for example:
    scp -r path/to/project/directory raspberry@192.168.0.11:/destination

#####set an environment variable COMPANY_ID with some random string:

    from the terminal, ssh into the raspberry pi and run the following commands:
    nano ~/.bash_profile
    this will open up an editor; add this line at the end of the file
    export COMPANY_ID = <SOME RANDOM VALUE>
    hit cmd+x and enter y to save changes
    
#####set the urls for the script to send the data to:

    open up the project in any text editor and navigate to base > Config.py
    change the variable BASE_ADDR to the base address of the server you want to data to be sent
    change the variable NODE_ADDR where the data regarding the nodes will be send at every fixed interval
    change the variable LOG_ADDR to where the log data will be sent at every fixed interval
    
#####set up cron jobs to execute main.py and log.py at fixed intervals:

    after connecting to the pi via ssh, type crontab -e
    An editor will show up; add these two lines at the bottom of the file
        */15 * * * * . ~/.bash_profile; python path/to/project/directory/main.py
        01 */1 * * * . ~/.bash_profile; python path/to/project/directory/ping.py
    Hit ctrl+x and then type 'y' and hit enter to save changes to the file. You should see the message 'new cronjobs are installed'.
    the breakdown of the cronjob is as follows (from left to right) minute - hour - day of week - month - year - /path/to/script

####Automate the process
To automate the whole process, there is a bash script DeployementReady.sh present in the repo. On it's execution, it will: 

    ask for a company id and automatically and set the environment variable
    
    download the latest version of the script from this repo
    
    install all the dependencies
    
    set up cron jobs to be executed at a fixed interval (send node data every 15 minutes - send log data every hour)