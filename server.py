import http.server
import socketserver
import requests
import sqlite3
import json
import nltk
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from urllib.parse import unquote
import speech_recognition as sr
import urllib.parse
from test2 import create_tables, signup, login

nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

# define the base URL for the Wikipedia API
base_url = "https://en.wikipedia.org/w/api.php"

# define the maximum number of categories to retrieve
MAX_CATEGORIES = 5

# define the Pixabay API key and base URL
PIXABAY_API_KEY = "36673726-42f596b4c4d016e77af5655d6"
PIXABAY_BASE_URL = "https://pixabay.com/api/"

# define the request handler class
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def insert_data(self, links):
        # connect to the SQLite database and create a cursor object
        mydb = sqlite3.connect('wikipedia.db')
        mycursor = mydb.cursor()
        # get all the article titles, texts, and snippets
        titles = []
        texts = []
        snippets = []
        for link in links:
            title = link["title"]
            url = "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")
            # check if the link already exists in the database
            sql = "INSERT OR IGNORE INTO wikipedia (title, links) VALUES (?, ?)"
            val = (title, url)
            mycursor.execute(sql, val)
            # scrape the text of the article using BeautifulSoup
            soup = BeautifulSoup(requests.get(url).content, "html.parser")
            text = soup.get_text()
            # preprocess the text by removing stop words
            text = " ".join([word for word in text.split() if word.lower() not in stop_words])
            # retrieve a snippet of the article text
            snippet = soup.select_one(".searchsnippet")
            if snippet:
                snippet = snippet.text.strip()
            else:
                snippet = ""
            titles.append(title)
            texts.append(text)
            snippets.append(snippet)
        # compute the tf-idf matrix
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(texts)
        # compute the cosine similarity matrix
        cosine_sim_matrix = cosine_similarity(tfidf_matrix)
        # compute the tf-idf ranking for each article
        for i in range(len(links)):
            title = titles[i]
            url = "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")
            categories = []
            # scrape the categories of the article using BeautifulSoup
            soup = BeautifulSoup(requests.get(url).content, "html.parser")
            for element in soup.select(".mw-normal-catlinks ul li a"):
                categories.append(element.text)
                if len(categories) == MAX_CATEGORIES:
                    break
            # join the categories into a comma-separated string
            category = ", ".join(categories)[:255]  # truncate the category string to fit the maximum length
            # compute the tf-idf ranking using the cosine similarity matrix
            tfidf_ranking = cosine_sim_matrix[i].sum()
            # get the snippet of the article
            snippet = snippets[i]
            sql = "UPDATE wikipedia SET category = ?, snippet = ?, tfidf_ranking = ? WHERE links = ?"
            val = (category, snippet, tfidf_ranking, url)
            mycursor.execute(sql, val)
        mydb.commit()
        mydb.close()

    def insert_image_data(self, query, images):
        # connect to the SQLite database and create a cursor object
        mydb = sqlite3.connect('image_search.db')
        mycursor = mydb.cursor()
        # insert the image data into the database
        for image in images:
            url = image["webformatURL"]
            tags = image["tags"]
            # check if the image already exists in the database
            sql = "INSERT OR IGNORE INTO images (query, url, tags) VALUES (?, ?, ?)"
            val = (query, url, tags)
            mycursor.execute(sql, val)
        mydb.commit()
        mydb.close()

    def search_images(self, query):
        # check if the search query exists in the database
        sql = "SELECT * FROM images WHERE query = ?"
        val = (query,)
        mydb = sqlite3.connect('image_search.db')
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        rows = mycursor.fetchall()
        mydb.close()
        if len(rows) > 0:
            # retrieve the search results from the database
            results = []
            for row in rows:
                result = {"url": row[2], "tags": row[3]}
                results.append(result)
            return results
        else:
            # perform the image search using the Pixabay API
            params = {
                "key": PIXABAY_API_KEY,
                "q": query,
                "per_page": 10,
                "image_type": "photo"
            }
            response = requests.get(PIXABAY_BASE_URL, params=params).json()
            # extract the images from the response
            images = response["hits"]
            # insert the image data into the database
            self.insert_image_data(query, images)
            return images

    def do_GET(self):
        if self.path == '/':
            # serve the home page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path.startswith('/search'):
            # parse the search query from the URL
            search_query = unquote(self.path.split('=')[1]).strip()
            # split the search query into individual queries
            search_queries = [search_query]
            # initialize the results list
            results = []
            for query in search_queries:
                # check if the search query has already been searched before
                sql = "SELECT * FROM wikipedia WHERE title LIKE ?"
                val = ("%" + query.strip() + "%",)
                mydb = sqlite3.connect('wikipedia.db')
                mycursor = mydb.cursor()
                mycursor.execute(sql, val)
                rows = mycursor.fetchall()
                mydb.close()
                if len(rows) > 0:
                    # retrieve the search results from the database
                    for row in rows:
                        result = {"title": row[1], "category": row[2], "snippet": row[4]}
                        results.append(result)
                else:
                    # define the parameters for the API request
                    params = {
                        "action": "query",
                        "format": "json",
                        "list": "search",
                        "srsearch": query.strip(),
                        "utf8": 1,
                        "srlimit": 100
                    }
                    # send the API request and retrieve the JSON response
                    response = requests.get(base_url, params=params).json()
                    # extract the titles and URLs of the articles from the response
                    articles = response["query"]["search"]
                    # divide the links into batches of 10
                    batches = [articles[i:i + 10] for i in range(0, len(articles), 10)]
                    # insert the data into SQLite in batches
                    for batch in batches:
                        self.insert_data(batch)
                    # retrieve the search results from SQLite
                    mydb = sqlite3.connect('wikipedia.db')
                    mycursor = mydb.cursor()
                    mycursor.execute(sql, val)
                    rows = mycursor.fetchall()
                    mydb.close()
                    for row in rows:
                        result = {"title": row[1], "category": row[2], "snippet": row[4]}
                        results.append(result)
            # send the search results as JSON
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(results).encode())
        elif self.path.startswith('/image-search'):
            # parse the search query from the URL
            search_query = unquote(self.path.split('=')[1]).strip()
            # search for images using the Pixabay API
            images = self.search_images(search_query)
            # send the image search results as JSON
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(images).encode())
        elif self.path == '/speech-to-text':
            # perform speech-to-text conversion
            recognized_query = self.speech_to_text()
            # redirect to the search page with the recognized query
            self.send_response(302)
            self.send_header('Location', '/search?q=' + recognized_query)
            self.end_headers()
        else:
            # serve the static files
            http.server.SimpleHTTPRequestHandler.do_GET(self)

    def speech_to_text(self):
        # define the recognizer and microphone instances
        r = sr.Recognizer()
        mic = sr.Microphone()

        try:
            print("Listening...")
            with mic as source:
                # adjust for ambient noise
                r.adjust_for_ambient_noise(source)
                # listen to the user's input
                audio = r.listen(source)
            print("Recognizing...")
            # convert speech to text using Google Speech Recognition
            query = r.recognize_google(audio)
            print("Recognized query:", query)
            return query
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return


# define the main function
def main():
    # create a TCP/IP socket
    socketserver.TCPServer.allow_reuse_address = True
    # set up the server
    server = socketserver.TCPServer(("", 7112), MyRequestHandler)
    # start the server and keep it running
    print("Server running on port 7112...")
    server.serve_forever()


# run the main function
if __name__ == "__main__":
    main()
