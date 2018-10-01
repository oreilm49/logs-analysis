# Log Analysis Project
A reporting tool that prints out reports (in plain text) based on the data in a database using python.

<b>Built with</b>
- Python 3
- Postgresql

## Usage
<b>PreRequisites</b>
- Python3
- Vagrant
- VirtualBox
- Postgresql

<b>Setup</b>
1. Set up a new directory
    ~~~~
    mkdir reporting-project && cd reporting-project
    ~~~~
1. [Install vagrant](https://www.vagrantup.com/docs/installation/)
2. [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads)
3. [Download](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and unzip sql database into dir
3. Clone this repository
    ~~~~
    git clone https://github.com/oreilm49/logs-analysis
    ~~~~

<b>Run</b>
1. Launch Vagrant by & log in by running
    ~~~~
    > vagrant up
    > vagrant ssh
    ~~~~
2. Load database by running the following sql
    ~~~~
    psql -d news -f newsdata.sql
    ~~~~
3. Run database analysis
    ~~~~
    python reporting.py
    ~~~~

## Under the hood
<b>Database</b>

There are three tables in the database
- Authors: contains information about article authors.
- Articles: all information on each article inluding content, slug, title and a foreign key linking to the Authors table.
- Log: Info relating to each individual page request per article. Describes each request by URI path, method, timestamp, ip and the HTTP status.

There are also two views:
- articles_info: creates a relationship between each article, it's author and number of views.
    ~~~~
    CREATE VIEW articles_info AS
        SELECT articles.title AS article,
        authors.name AS author, count(log.path)
        AS views
        FROM articles, authors, log
        WHERE CONCAT('/article/',articles.slug) =
        log.path AND articles.author = authors.id
        AND log.path LIKE '%/article/%'
        GROUP BY articles.title, authors.name
        ORDER BY views DESC;
    ~~~~
- day_requests: describes total number of requests per article page per day, and the total of each HTTP status.
    ~~~~
    CREATE VIEW day_requests AS
        SELECT time::date as day,
        count(*) FILTER (WHERE status = '200 OK')
        AS ok,
        count(*) FILTER (WHERE status = '404 NOT
        FOUND') AS bad,
        count(*) AS total
        FROM log
        GROUP BY day;
    ~~~~
<b>API</b>

Three functions provide insights on the database:
1. top3Articles() aptly named, returns the top three articles of all time.
2. topAuthors() returns the list of article authors ranked by article views.
3. notFoundRate() displays days where the % of page requests was above 1%.
