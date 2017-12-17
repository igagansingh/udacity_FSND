# Logs Analysis

Python file to test the understanding of database(s) basics and writing solution as per the specifications.

## Setting up the environment (views)

This file uses two views based on news database
1. popularity (used in query1 and query2)
2. perror_view (used in query3)
### 1. popularity

```
create view popularity as select articles.title, articles.author, count(log.path) as views from articles join log on log.path like concat('%', articles.slug) group by articles.title, articles.author order by views desc;
```

### 2. perror_view

```
create view perror_view as select date(time), round(100.0*sum(case when log.status like '200 OK' then 0 else 1 end)/count(log.status),2) as perror from log group by date(time) order by perror desc;
```
## Running the python file

Open the terminal, navigate to the folder containing 'log_analysis.py' file and give python command to run this  file.

```
$ python log_analysis.py
```