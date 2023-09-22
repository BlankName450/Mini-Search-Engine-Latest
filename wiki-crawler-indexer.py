import requests
import mysql.connector
from bs4 import BeautifulSoup

# define the search query
search_query = "محمد علي باشا"

# define the base URL for the Wikipedia API
base_url = "https://en.wikipedia.org/w/api.php"

# define the parameters for the API request
params = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": search_query,
    "utf8": 1,
    "srlimit": 100
}

# send the API request and retrieve the JSON response
response = requests.get(base_url, params=params).json()

# extract the titles and URLs of the articles from the response
articles = response["query"]["search"]

# divide the links into batches of 10
batches = [articles[i:i+10] for i in range(0, len(articles), 10)]
# connect to the MySQL database
mydb = mysql.connector.connect(
    user="root", password="1234", database="research_ms"
)
create_table_query = f"""CREATE TABLE IF NOT EXISTS wikipedia (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255)  NULL,
    category VARCHAR(255)  NULL,
    links VARCHAR(767)  NULL,
    UNIQUE(links)
)"""
mycursor = mydb.cursor()
mycursor.execute(create_table_query)

# define a function to insert the data into MySQL
def insert_data(links):

    for link in links:
        title = link["title"]
        url = "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")
        # scrape the categories of the article using BeautifulSoup
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        categories = []
        for element in soup.select(".mw-normal-catlinks ul li a"):
            categories.append(element.text)
        # join the categories into a comma-separated string
        category = ", ".join(categories)[:255] # truncate the category string to fit the maximum length
        sql = "INSERT INTO wikipedia (title, links, category) VALUES (%s, %s, SUBSTRING(%s, 1, 255))"
        val = (title, url, category)
        mycursor.execute(sql, val)
    mydb.commit()

# insert the data into MySQL in batches
for batch in batches:
    insert_data(batch)

print("Data inserted into MySQL successfully!")