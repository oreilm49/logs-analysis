#!/usr/bin/env python3

import psycopg2
import datetime

conn = psycopg2.connect("dbname=news")


# 1 - what are the most popular 3 articles of all time?
def top3Articles():
    q = "SELECT * FROM articles_info LIMIT 3;"
    c = conn.cursor()
    c.execute(q)
    articlesStr = ""

    for a in c.fetchall():
        article, author, views = a
        string = str(article)+" - "+str(views)+" views\n"
        articlesStr += string
    c.close()
    print("Top 3 Articles: \n"+articlesStr+"\n")


# 2 - who are the most popular article authors of all time?
def topAuthors():
    q = """SELECT author, sum(views) as views from articles_info
        GROUP BY author
        ORDER BY views DESC;"""
    c = conn.cursor()
    c.execute(q)
    authorsStr = ""

    for i in c.fetchall():
        author, views = i
        string = str(author)+" - "+str(views)+" views\n"
        authorsStr += string
    c.close()
    print("Top Authors:\n"+authorsStr+"\n")


# 3 - on which days did more than 1% of requests lead to errors?
def notFoundRate():
    q = """SELECT day, (bad*1.0)/(total*1.0) AS badPC FROM day_requests
        WHERE (bad*1.0)/(total*1.0) >= 0.01
        ORDER BY badpc DESC;"""
    c = conn.cursor()
    c.execute(q)
    requestsStr = ""

    for i in c.fetchall():
        date, pc = i
        month = str(date.strftime("%B"))
        dateString = month+" "+str(date.day)+", "+str(date.year)
        requestsStr += dateString+" - "+"{:.2%}".format(pc)+' errors'
    c.close()
    print("Days where 404 error rate > 1%\n"+requestsStr)


top3Articles()
topAuthors()
notFoundRate()
