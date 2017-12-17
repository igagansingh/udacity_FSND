import psycopg2

"""
views used

1.  popularity (used in query1 and query2)
>   create view popularity as select articles.title, articles.author, count(log.path) as views from articles join log on log.path like concat('%', articles.slug) group by articles.title, articles.author order by views desc;  # noqa

2.  perror_view (used in query3)
>   create view perror_view as select date(time), round(100.0*sum(case when log.status like '200 OK' then 0 else 1 end)/count(log.status),2) as perror from log group by date(time) order by perror desc;  # noqa

"""
DB = "news"

query1 = "select title, views from popularity limit 3"
query2 = "select authors.name, sum(views) as views from popularity,authors where author=authors.id group by authors.name order by views desc"  # noqa
query3 = "select * from perror_view where perror > 1"

db = psycopg2.connect(database=DB)
c = db.cursor()

# Query 1
print("\n1. What are the most popular three articles of all time?\n")

c.execute(query1)
result = c.fetchall()

print("Title of article\t\t\t\tViews")
print("------------------------------------------------------------")
for title, views in result:
    print("{}\t\t{}".format(title, views))

# Query 2
print("\n2. Who are the most popular article authors of all time?\n")

c.execute(query2)
result = c.fetchall()

print("Author Name\t\t\tViews")
print("------------------------------------------------------------")
for author, views in result:
    print("{}\t\t\t{}".format(author, views))

# Query 3
print("\n3. On which dates did more than 1% of requests lead to errors?\n")

c.execute(query3)
result = c.fetchall()

print("Author Name\t\t\tViews")
print("------------------------------------------------------------")

for author, views in result:
    print("{}\t\t\t{}".format(author, views))

db.close()
