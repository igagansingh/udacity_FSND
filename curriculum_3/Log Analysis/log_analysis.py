#!/usr/bin/env python3

import psycopg2

"""
views used

1.  Popularity (used in query1 and query2)
>   CREATE VIEW popularity AS
    SELECT articles.title, articles.author, count(log.path) as views
    FROM articles JOIN log on log.path = '/article/' || articles.slug
    GROUP BY articles.title, articles.author
    ORDER BY views DESC;

2.  Error (used in query3)
>   CREATE VIEW perror_view AS
    SELECT date(time), round(100.0*sum(case when log.status like '200 OK'
    then 0 else 1 end)/count(log.status),2) as perror
    FROM log
    GROUP BY date(time)
    ORDER BY perror DESC;
"""
DBNAME = "news"


def db_connect():
    """ Creates and returns a connection to the database defined by DBNAME,
        as well as a cursor for the database.

        Returns:
            db, c - a tuple. The first element is a connection to the database.
                    The second element is a cursor for the database.
    """

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    return db, c


def execute_query(query):
    """execute_query takes an SQL query as a parameter.
        Executes the query and returns the results as a list of tuples.
        args:
            query - an SQL query statement to be executed.
        returns:
            A list of tuples containing the results of the query.
    """

    db, c = db_connect()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


def print_top_articles():
    """Prints out the top 3 articles of all time."""

    query = '''SELECT title, views
            FROM popularity
            LIMIT 3'''
    result = execute_query(query)
    print('{0:<30}{1:^13}'.format('Title of article', 'Views'))
    print("-" * 50)
    for title, views in result:
        print("{0:<30}{1:>8} views".format(title, views))


def print_top_authors():
    """Prints a list of authors ranked by article views."""

    query = '''SELECT authors.name, sum(views) AS views
            FROM popularity, authors
            WHERE author=authors.id
            GROUP BY authors.name
            ORDER BY views DESC'''
    result = execute_query(query)
    print('{0:<30}{1:^13}'.format('Author Name', 'Views'))
    print('-' * 50)
    for author, views in result:
        print('{0:<30}{1:>8} views'.format(author, views))


def print_errors_over_one():
    """Prints out the days where more than 1% of logged access
        requests were errors."""

    query = '''SELECT *
            FROM perror_view
            WHERE perror > 1'''
    result = execute_query(query)
    print('{0:<24}{1:^13}'.format('Date', 'Percentage Error'))
    print("-" * 50)
    for date, perror in result:
        print("{:%B %d, %Y}\t\t\t{} %".format(date, perror))

if __name__ == '__main__':
    # Query 1
    print("\n1. What are the most popular three articles of all time?\n")
    print_top_articles()
    # Query 2
    print("\n2. Who are the most popular article authors of all time?\n")
    print_top_authors()
    # Query 3
    print("\n3. On which days did more than 1% of requests lead to errors?\n")
    print_errors_over_one()
