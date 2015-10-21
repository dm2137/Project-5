<<<<<<< HEAD
Readme file for Project 5 of the Udacity Full Stack Web Developer Nanodegree.


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
______________________________________________________
http://www.hcidata.info/host2ip.cgi

IP Address: 54.148.70.58

Location   : United States (95% accuracy)

Host Name  : ec2-54-148-70-58.us-west-2.compute.amazonaws.com

Details of Computer Using This Web Service

Below is shown the name of the computer that is using this web service. If this computer is behind a firewall or uses a proxy server, the name shown will be that of the firewall  -computer or proxy server. Many ISPs route internet traffic via a proxy server to reduce network traffic. Most commercial organisations protect their internal network (Intranet) by routing all traffic to and from the Internet via a firewall. A firewall computer of proxy server is sometimes called a 'gateway'.

IP Address : 172.11.73.3
Host Name  : 172-11-73-3.lightspeed.cicril.sbcglobal.net		

_________________________________________________________________
Vagrantfile: 
config.vm.box = "ubuntu/trusty64"
  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 80, host:8080, auto_correct: true
  config.vm.network "forwarded_port", guest: 2200, host: 2200, id: "ssh"
  config.ssh.port = 2200 
end		


catalog.wsgi:
		
		!/usr/bin/python
		import sys
		import logging
		logging.basicConfig(stream=sys.stderr)
		sys.path.insert(0,"/var/www/catalog/catalog")
		
		from catalog import app as application
		application.secret_key = 'super_secret_key'
		
		
/etc/apache2/sites-available/catalog.conf    #(configures virtual host)
	
	<VirtualHost *:80>
	        ServerName localhost
	        WSGIScriptAlias / /var/www/catalog/catalog.wsgi
	        <Directory /var/www/catalog/catalog/>
	                Order allow,deny
	                Allow from all
	        </Directory>
	        Alias /static /var/www/catalog/catalog/static
	        <Directory> /var/www/catalog/catalog/static/>
	                Order allow,deny
	                Allow from all
	        </Directory>
	        ErrorLog ${APACHE_LOG_DIR}/error.log
	        LogLevel warn
	        CustomLog ${APACHE_LOG_DIR}/access.log combined
	</VirtualHost>
	
			
Changed ssh port in /etc/ssh/sshd_config
	from Port 22  =>  change to 2200

Created new user named grader with sudo permissions;  
		password for grader is full15nan0  

Updates all currently installed packages
   sudo apt-get upgrade


Configured the local timezone to UTC

Created a POSTGRESQL user/role named catalog with limited permissions to the database (i.e. NOSUPERUSER)
                             List of roles
 Role name |                   Attributes                   | Member of
-----------+------------------------------------------------+-----------
 catalog   | Create role, Create DB                         | {}
 postgres  | Superuser, Create role, Create DB, Replication | {}

Updated my Catalog project to utilize POSTGRESQL vs SQLlite.  Catalog application working great on the localhost:8080

Configured the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)

---------------------------------------------------------
My Amazon EC2 Instance public URL is:ec2-52-10-245-33.us-west-2.compute.amazonaws.com

I was able to link my computer with Amazon's EC2 environment:
Deborah (master) Linux $ ssh -i ~/fullstack/vagrant/Linux/catalog-key-pair-uswe
st2.pem ec2-user@ec2-52-10-245-33.us-west-2.compute.amazonaws.com
The authenticity of host 'ec2-52-10-245-33.us-west-2.compute.amazonaws.com (52.1
0.245.33)' can't be established.
ECDSA key fingerprint is b9:07:a6:d0:fd:27:cc:d7:7d:de:ab:4d:7d:95:c5:29.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'ec2-52-10-245-33.us-west-2.compute.amazonaws.com,52.
10.245.33' (ECDSA) to the list of known hosts.

       __|  __|_  )
       _|  (     /   Amazon Linux AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-ami/2015.09-release-notes/
No packages needed for security; 14 packages available
Run "sudo yum update" to apply all updates.
[ec2-user@ip-10-0-0-46 ~]$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/xvda1      7.8G  1.1G  6.6G  14% /
devtmpfs        489M   56K  489M   1% /dev
tmpfs           498M     0  498M   0% /dev/shm
[ec2-user@ip-10-0-0-46 ~]$

-------------------------------------------------------

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

PRIVATE KEY:

-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAxZdyWexJsPDsDNQOxE1SdtClTKYs3oZyTHAznBkYxkcQhRqx
30M2zy04Hmsqw05NSyjurc0uMA02uTMexZXHhzqy7/T91iGjWn55XR4turg/ypGM
ySXAWcACH9ufeJDDAhLmkyBze0iQjqApQCsQROM/nZdt2Ty5QYgJBnt6cMf8XiwM
osRqZKqCoB1kea5auvNr49A9yjKGK3j8iqNWrBc2mDEkKVjPQ+Ek190o0B99RMQC
Ve9a361h7RJGzZyhV8+qwWLFG8+fWWWues1TbfB54JwjM9xBmGaeJu3dNbpnnJQL
klWdsAJ4du+nbUuuwPXQ78fxEInrVpLdcgqBBQIDAQABAoIBAQDAj0MFl1yJb4Db
T53EeIYw/EzbUebQRb4F+CKTsXGPaZoT3VwS9HHpnWvfWRknlJuG77EK97ZXZck6
2zLV4427n9zaNKtbjxSfEDo+ITb3jK++PfIx5PR7gr+PRH05BfrFfp3uK+Xe82zN
UhBhVJZaTAynC/gliSQRVP1Wr+c3GDfKfYYaNwbohl7X1+e0JSkWKHoQNWqbWACX
OcpNaC/sfNgrIFmHSNV0oABEDKL5NRi7liFR9cot0VSHETFsTgxBkzneG3UhOvl7
gHEb5EqAdhvNkd06m/elXegyqe3E5SXpiRQsfzrDlbr+bBk8JX//v21FZZUl9hL2
rVpXb/fRAoGBAOVTp31lNyUGO+cntUrfympOtMitHuZSqBiiUAl71+18XsdL7tHr
impM7BXNUnErpaqtzFjEuW6M6O1DOLIE4uBBN8QDuQ1UFvdSdCBW2FG7rP2oV96y
uqoAC+3lQjUGNudHgbMFFTYICr8M8Ie8JXvu0HyHba8OrHjBOMUyJbofAoGBANyS
25WrteTuiDsN+/FXhqt7vg0sZs8Fwna1tNDYsGPL7XQXhjPgUu/SPFaUnXKpLFvt
Hh8/5PzWxQYEhqwXFNHgWwaoSRsN3ZXukMsQlWA1UMJyJ8gaGRHPU06YySPadmxP
8fPHEbg2BMfoRtM2mPZvctRZJEvelFEq4APN46hbAoGBALCWPxXW96Sh7UStFfPm
6bX8j0crz+xpX5lAe0MiQv5TU6RBe0/YAQij3PNY3I/anUIVfJIqQeO3y7DPn3ut
OYqXjbp5Z2i1BM5DhrpURVSCoM3ecHNCy2wWhxkT/WxZMbPcIypX0qJ9hNDixOCw
Z2jMV2xc2IABW5vMpctrNxPfAoGBAMph5SB7ILYhNtYYiqZyTJpjO4oSx3IEMt2A
85r8dzvaDNGMFBLdLLvnBn3admySVKUz94NsuMpUtQpEdNzJgMzhMiP1nL46Bqpe
7nOjj6tqv+Lpox6y83Wn6SQgg81l0WqoH7QxX0zKI7DYqsN5QPg8Yfv8npUOcL/Y
uxpCezQpAoGAOtNKptafWzlyk7lA3zd6pPgWej6VM+fTdW4cN/jXu/BdFyyHuR7P
GCoaYlKGxk3JmNfyPi8XdzNlql2xCUg6WCiwxkRpIK1Ar9jV8p2+UwZQ6dWKmenF
wS85lZoD+whKq1TCMTGYrDJYw3D8qPcKxM8JZ2X8VG4ZtXbyBlfWb48=
-----END RSA PRIVATE KEY-----









