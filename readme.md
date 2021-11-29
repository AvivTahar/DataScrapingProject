### Linkedin Jobs Scraper
#### Made by Aviv Tahar and Evgeny Oyffe 
This project automatically opens a web driver and collects information from a 
linkdin job list defined by the user. The program inserts the job listings
to a predefined MySQL server.

How to use:
1. This program assumes the user has a MySQL server installed.
2. Type python db_init.py [username] [password] [ip]
with the MySQL servers username, password and ip as the arguments on your local 
Terminal. This should only be performed once since db_init.py creates a database
through the preinstalled MySQL server. Make sure you dont already have a 
database names 'jobs'
Example: python db_init.py root myPassword 127.0.0.1 

Let the program initiate the database

4. Type python main.py [serch_query] [username] [password] [ip] on your terminal to
activate the scraper. 
Example: python main.py 'data scientist in beer sheva' root myPassword 127.0.0.1
Note that the user, password and ip should be the same as in phase 2. The given
example is supposed to perform a simple demonstration. 

The scraper will run the search query on google for a linkedin job list on 
chrome incognito mode, it will scrape the different job listings it found and
insert it into the database.

PREREQUISITES: 
1. Download and install chromedriver before running this project
by following the setup section on this link: 
https://chromedriver.chromium.org/getting-started

2. Install requirements `pip install -r /path/to/requirements.txt`

Remote repo:  https://github.com/AvivTahar/DataScrapingProject.git

DataBase Information:
The database was designed to accept the different job listings and keep track
of the jobs, companies, cities, countries, seniority level, employment type,
job functions and industries

Most tables except jobs and cities are short tables with a few specific possible
entries. 
cities table holds the current information of location of jobs and a foreign key
to the countries table. The cities are unique in such way that a unique city
also is specific for a country. For Example: Moscow, Russia and Moscow, USA 
are unique cities.
jobs table is the major table of our database and holds unique job entries 
with information relating it to the other tables. 

Entity Relation Diagram (ERD):
img![](C:\Users\user\PycharmProjects\pythonProject6\scraping_db-1.jpg)