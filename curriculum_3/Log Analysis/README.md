# Logs Analysis

Python file that answers few questions about a news database. Database here is a PostgreSQL, it consist of 3 tables.
	Articles - Contains information about a article and who has written it (ID of author).
	Authors	 - Contains information about a author, each author has an ID(unique).
	Log 	 - Contains a log of requests made to this website (and articles), request status and other details.

## Requirements

This project uses Linux-based virtual machine 

1. VirtualBox (https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
2. Vagrant (https://www.vagrantup.com/downloads.html)
3. News database(https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

## Setting up the environment (views)

1. Download the VM configuration(https://github.com/udacity/fullstack-nanodegree-vm)
2. Once the configuration is up navigate to vagrant folder, and start the virtual machine using:
	> vagrant up (This will cause Vagrant to download the Linux operating system and install it.)
	> vagrant ssh (To log in to your newly installed Linux VM)

3. You need to create two views for the file to run successfully
	
	##### popularity (used in query1 and query2)

	```sql
	CREATE VIEW popularity AS
    SELECT articles.title, articles.author,	count(log.path) as views
    FROM articles JOIN log on log.path = '/article/' || articles.slug
    GROUP BY articles.title, articles.author
    ORDER BY views DESC;
	```

	##### perror_view (used in query3)

	```sql
	CREATE VIEW perror_view AS
    SELECT date(time), round(100.0*sum(case when log.status like '200 OK'
    then 0 else 1 end)/count(log.status),2) as perror
    FROM log
    GROUP BY date(time)
    ORDER BY perror DESC;
	```

## Running the python file

After succesfully setting the virtual environment, database and views, open the terminal, navigate to the folder containing 'log_analysis.py' file and give python command to run this  file.

```
$ python log_analysis.py
```