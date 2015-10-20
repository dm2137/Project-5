Readme file for Project 3 of the Udacity Full Stack Web Developer Nanodegree.


A virtual machine (VM) is used to run a database server and a web app that uses it. The VM is a Linux server system that runs on 
top of your own computer.  You can share files easily between your computer and the VM.


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


5) Running the Catalog App

While in VM, change directory to catalog (cd /vagrant/catalog)

Type ls to ensure that you are inside the directory that contains application.py, database_setup.py, and two directories named 'templates' and 'static'

Now type python database_setup.py to initialize the database.

Type python lotsofitems.py to populate the database with catalog items. (Optional)

Type python application.py to run the Flask web server. 

In your browser visit http://localhost:8000 to view the Catalog app.

There are four main parts to this project:
1)the HTML (structure of the pages)
2)the CSS (the style of the pages)
3)the Flask Application (to put it online)
	- use version 0.9 of Flask (pip install flask==0.9)
	This should avoid the error of: TypeError: <oauth2client.client.OAuth2Credentials object at 0xb5c9dccc> is not JSON serializable

4)it must include authentication/authorization to allow users to login before making changes
the database (to store and organize the information)

This project is a web application that provides a list of items within a variety of categories 
and integrate third party user registration and authentication. Authenticated users should have the ability to post, edit, 
and delete their own items.

JSON API Endpoint (GET Request):
	APIs that return JSON objects have been included for a list of the categories in the catalog,
		and the specific items in an identified category.

		- to view catalog info, go to '/catalog/JSON/'
		- for items in category, go to '/catalog/<int:catalog_id>/items/JSON/'

