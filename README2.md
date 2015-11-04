<<<<<<< HEAD
Readme file for Project 5 of the Udacity Full Stack Web Developer Nanodegree.

++++++++++++++++++++++++++++++
Notes:  A known issue at this point:
	1) I'm getting a 400 error when authenticating with Google.  Facebook works fine.
	
+++++++++++++++++++++++++++++++++++++++++++

TOOL REQUIREMENTS:

A virtual machine (VM) is used to run a database server and a web app that uses it. The VM is a Linux server system that runs on top of your own computer.  You can share files easily between your computer and the VM.

The Vagrant software is used to configure and manage the VM. 

The following outlines the tools you'll need to install to get the VM running:

1) Git:

If you don't already have Git installed, download Git from git-scm.com. Install the version for your operating system.

On Windows, Git will provide you with a Unix-style terminal and shell (Git Bash).
(On Mac or Linux systems you can use the regular terminal program.)

You will need Git to install the configuration for the VM. If you'd like to learn more about Git, take a look at our course about Git and Github.


2) VirtualBox:

VirtualBox is the software that actually runs the VM. 

You can download it from virtualbox.org, at the following link: https://www.virtualbox.org/wiki/Downloads 

Install the platform package for your operating system.  You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.

Ubuntu 14.04 Note: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center, not the virtualbox.org web site. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.


3) Vagrant:

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem.  
You can download it from https://www.vagrantup.com/downloads. Install the version for your operating system.

Windows Note: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.
Use Git to fetch the VM configuration

Windows: Use the Git Bash program (installed with Git) to get a Unix-style terminal.
Other systems: Use your favorite terminal program.

From the terminal, run:

         git clone http://github.com/udacity/fullstack-nanodegree-vm fullstack

This will give you a directory named fullstack.


4) Run the virtual machine:

Using the terminal, change directory to fullstack/vagrant (cd fullstack/vagrant), 
then type "vagrant up" to launch your virtual machine.
Once it is up and running, type vagrant ssh. 

This will log your terminal in to the virtual machine, and you'll get a Linux shell prompt. 

The Vagrant VM provided in the fullstack repo already has PostgreSQL server installed, as well as the psqul command line interface(CLI).

When you want to log out, type "exit" at the shell prompt.  To turn the virtual machine off (without deleting anything), type "vagrant halt". If you do this, you'll need to run "vagrant up" again before you can log into it.

5) Install and configure Apache to serve a Python mod_wsgi application
6) Install and configure PostgreSQL
++++++++++++++++++++++++++++++++++++++++++++++
DIRECTORY STRUCTURE:
/var
	/www
		/catalog
			/catalog
				/static
				/templates
				/catalog.py
				/client_secrets.json
				/database_setup.py
				/fb_client_secrets.json
				/__init__.py
				/lotsofitems.py
				
				/venv
		/catalog.wsgi
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

Public IP Address : 52.32.13.248

Location   : United States (95% accuracy)

Host Name  : ec2-52-32-13-248.us-west-2.compute.amazonaws.com

IP Address : 172.11.73.3
Host Name  : 172-11-73-3.lightspeed.cicril.sbcglobal.net		

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Project steps:
------
1 & 2 - Create Development Environment: Launch Virtual Machine and SSH into the server
	1. Create new development environment.
	2. Download private keys and write down your public IP address.
	3. Move the private key file into the folder ~/.ssh:
		$ mv ~/Downloads/udacity_key.rsa ~/.ssh/
	4. Set file rights (only owner can write and read.):
		$ chmod 600 ~/.ssh/udacity_key.rsa
	5. SSH into the instance:
		<pre>$ ssh -i ~/.ssh/udacity_key.rsa root@PUPLIC-IP-ADDRESS
-----
3 & 4 - User Management: Create a new user and give user the permission to sudo
	1. Create a new user:
		$ adduser NEWUSER
	2. Give new user the permission to sudo
		1. Open the sudo configuration:
			$ visudo
		2. Add the following line below root ALL...:
			NEWUSER ALL=(ALL:ALL) ALL
		3. *List all users (Source: Ask Ubuntu):
			$ cut -d: -f1 /etc/passwd
-----
5 - Update all currently installed packages
	1. Update the list of available packages and their versions:
		$ sudo apt-get update
-----
6 - Change the SSH port from 22 to 2200 and configure SSH access
	1. Change ssh config file:
		1. Open the config file:
			$ nano /etc/ssh/sshd_config
		2. Change to Port 2200.
		3. Change PermitRootLogin from without-password to no.
		4. * To get more detailed logging messasges, open /var/log/auth.log and change LogLevel from INFO to VERBOSE.
		5. Temporalily change PasswordAuthentication from no to yes.
		6. Append UseDNS no.
		7. Append AllowUsers NEWUSER.

	2. Restart SSH Service:
		$ /etc/init.d/ssh restart or # service sshd restart
	3. Create SSH Keys:
		1. Generate a SSH key pair on the local machine:
			$ ssh-keygen
		2. Copy the public id to the server:
			$ ssh-copy-id username@remote_host -p**_PORTNUMBER_**
		3. Login with the new user:
			$ ssh -v grader@PUBLIC-IP-ADDRESS -p2200
		4. Open SSHD config:
			$ sudo nano /etc/ssh/sshd_config
		5. Change PasswordAuthentication back from yes to no.
-----
7 - Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)
Source: Ubuntu documentation
	1. Turn UFW on with the default set of rules:
		$ sudo ufw enable
	2. *Check the status of UFW:
		$ sudo ufw status verbose
	3. Allow incoming TCP packets on port 2200 (SSH):
		$ sudo ufw allow 2200/tcp
	4. Allow incoming TCP packets on port 80 (HTTP):
		$ sudo ufw allow 80/tcp
	5. Allow incoming UDP packets on port 123 (NTP):
		$ sudo ufw allow 123/udp
-----
8 - Configure the local timezone to UTC
	1. Open the timezone selection dialog:
		$ sudo dpkg-reconfigure tzdata
	2. Then chose 'None of the above', then UTC.
-----	
9 - Install and configure Apache to serve a Python mod_wsgi application
	1. Install Apache web server:
		$ sudo apt-get install apache2
	2. Open a browser and open your public ip address, e.g. http://52.32.13.248/ - It should say 'It works!' on the top of the page.
	3. Install mod_wsgi for serving Python apps from Apache and the helper package python-setuptools:
		$ sudo apt-get install python-setuptools libapache2-mod-wsgi
	4. Restart the Apache server for mod_wsgi to load:
		$ sudo service apache2 restart
-----	
10 - Install git, clone and setup your Catalog App project
	
10.1 - Install and configure git
	1. Install Git:
		$ sudo apt-get install git
	2. Set your name, e.g. for the commits:
		$ git config --global user.name "YOUR NAME"
	3. Set up your email address to connect your commits to your account:
		$ git config --global user.email "YOUR EMAIL ADDRESS"
10.2 - Setup for deploying a Flask Application on Ubuntu VPS
	1. Extend Python with additional packages that enable Apache to serve Flask applications:
		$ sudo apt-get install libapache2-mod-wsgi python-dev
	2. Enable mod_wsgi (if not already enabled):
		$ sudo a2enmod wsgi
	3. Create a Flask app:
		1. Move to the www directory:
			$ cd /var/www
		2. Setup a directory for the app, e.g. catalog:
			1. $ sudo mkdir catalog
			2. $ cd catalog and $ sudo mkdir catalog
			3. $ cd catalog and $ sudo mkdir static templates
			4. Create the file that will contain the flask application logic:
				$ sudo nano __init__.py
			5. Paste in the following code:
  				from flask import Flask  
  				app = Flask(__name__)  
  				@app.route("/")  
  				def hello():  
    			return "Veni vidi vici!!"  
  				if __name__ == "__main__":  
    				app.run()  
	4. Install Flask
		1. Install pip installer:
			$ sudo apt-get install python-pip
		2. Install virtualenv:
			$ sudo pip install virtualenv
		3. Set virtual environment to name 'venv':
			$ sudo virtualenv venv
		4. Enable all permissions for the new virtual environment (no sudo should be used within):
			$ sudo chmod -R 777 venv
		5. Activate the virtual environment:
			$ source venv/bin/activate
		6. Install Flask inside the virtual environment:
			$ pip install Flask
		7. Run the app:
			$ python __init__.py
		8. Deactivate the environment:
			$ deactivate
	5. Configure and Enable a New Virtual Host#
		1. Create a virtual host config file
			$ sudo nano /etc/apache2/sites-available/catalog.conf
		2. Paste in the following lines of code and change names and addresses regarding your application:
		  <VirtualHost *:80>
		      ServerName PUBLIC-IP-ADDRESS
		      ServerAdmin admin@PUBLIC-IP-ADDRESS
		      WSGIScriptAlias / /var/www/catalog/catalog.wsgi
		      <Directory /var/www/catalog/catalog/>
		          Order allow,deny
		          Allow from all
		      </Directory>
		      Alias /static /var/www/catalog/catalog/static
		      <Directory /var/www/catalog/catalog/static/>
		          Order allow,deny
		          Allow from all
		      </Directory>
		      ErrorLog ${APACHE_LOG_DIR}/error.log
		      LogLevel warn
		      CustomLog ${APACHE_LOG_DIR}/access.log combined
		  </VirtualHost>
		3. Enable the virtual host:
			$ sudo a2ensite catalog
	
	6. Create the .wsgi File and Restart Apache
		1. Create wsgi file:
			$ cd /var/www/catalog and $ sudo nano catalog.wsgi
		2. Paste in the following lines of code:
		  #!/usr/bin/python
		  import sys
		  import logging
		  logging.basicConfig(stream=sys.stderr)
		  sys.path.insert(0,"/var/www/catalog/")
		  
		  from catalog import app as application
  		  application.secret_key = 'Add your secret key'
			
		1. Restart Apache:
			$ sudo service apache2 restart

10.3 - Clone GitHub repository and make it web inaccessible
	1. Clone project 3 solution repository on GitHub:
		$ git clone https://github.com/xxxxxx
	2. Move all content of created catalog directory to/var/www/catalog/catalog/-directory and delete the leftover empty directory.
	3. Make the GitHub repository inaccessible:
		1. Create and open .htaccess file:
			$ cd /var/www/catalog/ and $ sudo nano .htaccess
		2. Paste in the following:
			RedirectMatch 404 /\.git

10.4 - Install needed modules & packages
	1. Activate virtual environment:
		$ source venv/bin/activate
	2. Install httplib2 module in venv:
		$ pip install httplib2
	3. Install requests module in venv:
		$ pip install requests
	4. Install flask.ext.seasurf
		$ sudo pip install flask-seasurf
	5. Install oauth2client.client:
		$ sudo pip install --upgrade oauth2client
	6. Install SQLAlchemy:
		$ sudo pip install sqlalchemy
	7. Install the Python PostgreSQL adapter psycopg:
		$ sudo apt-get install python-psycopg2

10,5 - Install and configure PostgreSQL

	1. Install PostgreSQL:
		$ sudo apt-get install postgresql postgresql-contrib
	2. Check that no remote connections are allowed (default):
		$ sudo nano /etc/postgresql/9.3/main/pg_hba.conf
	3. Open the database setup file:
		$ sudo nano database_setup.py
	4. Change the line starting with "engine" to (fill in a password):
python engine = create_engine('postgresql://catalog:PW-FOR-DB@localhost/catalog')
	5. Change the same line in application.py respectively
	6. Create needed linux user for psql:
		$ sudo adduser catalog (choose a password)
	7. Change to default user postgres:
		$ sudo su - postgre   instead I used sudo -u postgres -I (do not need root access in etc/sudoers)
	8. Connect to the system:
		$ psql
	9. Add postgre user with password:
		1. Create user with LOGIN role and set a password:
		# CREATE USER catalog WITH PASSWORD 'PW-FOR-DB'; (# stands for the command prompt in psql)
		2. Allow the user to create database tables:
		# ALTER USER catalog CREATEDB;
		3. *List current roles and their attributes: # \du
	10. Create database:
		# CREATE DATABASE catalog WITH OWNER catalog;
	11. Connect to the database catalog # \c catalog
	12. Revoke all rights:
		# REVOKE ALL ON SCHEMA public FROM public;
	14. Grant only access to the catalog role:
		# GRANT ALL ON SCHEMA public TO catalog;
	15. Exit out of PostgreSQl and the postgres user:
		# \q, then $ exit
	16. Create postgreSQL database schema:
		$ python database_setup.py

10.6 - Run application
	1. Restart Apache:
		$ sudo service apache2 restart
	2. Open a browser and put in your public ip-address as url, e.g. 52.25.0.41 - if everything works, the application should come up
	3. *If getting an internal server error, check the Apache error files:
		1. View the last 20 lines in the error log: $ sudo tail -20 /var/log/apache2/error.log
		
10.7 - Get OAuth-Logins Working
	1. Open http://www.hcidata.info/host2ip.cgi and receive the Host name for your public IP-address, e.g. for 52.25.0.41, its ec2-52-25-0-41.us-west-2.compute.amazonaws.com
	2. Open the Apache configuration files for the web app: $ sudo nano /etc/apache2/sites-available/catalog.conf
	3. Paste in the following line below ServerAdmin:
	ServerAlias HOSTNAME, e.g. ec2-52-32-13-248.us-west-2.compute.amazonaws.com
	4. Enable the virtual host:
		$ sudo a2ensite catalog
	5. To get the Google+ authorization working:
		1. Go to the project on the Developer Console: https://console.developers.google.com/project
		2. Navigate to APIs & auth > Credentials > Edit Settings
		3. add your host name and public IP-address to your Authorized JavaScript origins and your host name + oauth2callback to Authorized redirect URIs, e.g. http://ec2-52-32-13-248.us-west-2.compute.amazonaws.com/oauth2callback
	6. To get the Facebook authorization working:
		1. Go on the Facebook Developers Site to My Apps https://developers.facebook.com/apps/
		2. Click on your App, go to Settings and fill in your public IP-Address including prefixed hhtp:// in the Site URL field
		3. To leave the development mode, so others can login as well, also fill in a contact email address in the respective field, "Save Changes", click on 'Status & Review'

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Resources used:
● https://www.digitalocean.com/community/tutorials/howtoaddanddeleteusersonanubuntu1404
vps
● https://www.digitalocean.com/community/tutorials/howtodeployaflaskapplicationonanubuntuv
ps
● https://www.digitalocean.com/community/tutorials/howtosecurepostgresqlonanubuntuvps
● https://help.ubuntu.com/community/SSH/OpenSSH/InstallingConfiguringTesting
● http://unix.stackexchange.com/questions/127886/howcanirestartthesshdaemononubuntu
● https://help.ubuntu.com/community/UbuntuTime#Using_the_Command_Line_.28terminal.29
● https://www.digitalocean.com/community/tutorials/initialserversetupwithubuntu1404
● https://help.ubuntu.com/community/UFW
● http://askubuntu.com/questions/59458/errormessagewhenirunsudounabletoresolvehostnone
● http://askubuntu.com/questions/256013/couldnotreliablydeterminetheserversfullyqualifieddom
ainname
● http://blog.udacity.com/2015/03/stepbystepguideinstalllamplinuxapachemysqlpythonubuntu.
html
● http://discussions.udacity.com/t/markedlyunderwhelmingandpotentiallywrongresourcelistforp5/
8587
● https://help.github.com/articles/generatingsshkeys/
● https://help.github.com/articles/setupgit/
● http://serverfault.com/questions/110154/whatsthedefaultsuperuserusernamepasswordforpostgr
esafteranewinstall










