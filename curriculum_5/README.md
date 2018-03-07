# Linux Configuration Project


## Gist of this project

This project includes information on launching a virtual linux machine on the [cloud](https://lightsail.aws.amazon.com/ "AWS lightsail"), making it act as a web server, launching one of the previous projects: [Item Catalog](https://github.com/igagansingh/udacity_FSND/tree/master/curriculum_3/Item%20Catalog "Source code @ GitHub") and securing the web server.


## Information about the server

     Public IP :  13.127.202.52
     SSH Port  :  2200
     User      :  grader
     Website   :  http://13.127.202.52/


## Setup and Installation

1. Make an account on [Amazon Lightsail](https://lightsail.aws.amazon.com/ "Lightsail login").

     - Log In
          * Create an instance
          * Pick your instance image :
                Select a platfotm  - Linux/Unix
                Select a blueprint - Ubuntu (OS only)           
          * Choose your instance plan (choose the lowest)
          * Name your instance
          * CREATE.

2. SSH into the server.
     - Download the SSH key (.pem file) from Account page.
     - Give the 644 permission to the .pem file
           sudo chmod 644 NAME_OF_FILE.pem

     - SSH into the server
           ssh -i /path/to/key.pem ubuntu@PUBLIC_IP_ADDRESS
3. Update all the packages
       sudo apt-get update && sudo apt-get upgrade
4. Change the SSH port from 22 to nnnn
     - SSH into the server.
     - Change the port number by changing the port number from 20 to 2200
           sudo nano /etc/ssh/sshd_config
           sudo service sshd restart
     - After doing the above step make sure to configure the Netwoking tab on lightsail, add another Firewall with Application as Custom and Protocol as TCP and Port Range as 2200.
     - Now SSH into the server by :
           ssh -i /path/to/key.pem -p 2200 ubuntu@PUBLIC_IP_ADDRESS
5. Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2222), HTTP (port 80), and NTP (port 123).
       sudo ufw allow 2200/tcp
       sudo ufw allow 80/tcp
       sudo ufw allow 123/tcp
       sudo ufw enable
6. Create a new user account named grader.
       sudo adduser grader
7. Give grader the permission to sudo.
     - Add the following text after typing the command below
     - "grader ALL=(ALL) NOPASSWD:ALL"
           sudo nano /etc/sudoers.d/grader
8. Create an SSH key pair for grader using the ssh-keygen tool
     - Follow the instructions in the video below and store the public key in grader .ssh folder.
     - https://www.youtube.com/watch?v=k5JTVI6c7w8
9. Configure the local timezone to UTC
       sudo dpkg-reconfigure tzdata
10. Install and configure a serve to serve a Python application.
     - [How To Serve Flask Applications with uWSGI and Nginx on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04)
11. Install and configure PostgreSQL:
     - [Configure PostgreSQL on Ubuntu 16.04 ](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04)
12. Deploy the Item Catalog project
     - Get yout Item Catalog project from GitHub as submitted
     - Most important part to remember is to change the engine in your flask application from sqlite to postgresql

### Resources

- https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04
- [Use journalctl for checking logs in case of errors](https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs)
