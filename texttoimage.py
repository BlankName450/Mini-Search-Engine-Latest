import requests
import sqlite3
import json

# Set your Pixabay API key
API_KEY = "YOUR_PIXABAY_API_KEY"

# Define the base URL for the Pixabay API
BASE_URL = "https://pixabay.com/api/"

# Define the maximum number of images to retrieve
MAX_IMAGES = 10

# Create a database if it doesn't exist and create the tables
def create_database():
    # Connect to the SQLite database and create a cursor object
    mydb = sqlite3.connect('texttoimage.db')
    mycursor = mydb.cursor()

    # Create the images table if it doesn't exist
    mycursor.execute('''CREATE TABLE IF NOT EXISTS images
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        query TEXT NOT NULL,
                        image_url TEXT NOT NULL,
                        preview_url TEXT NOT NULL,
                        tags TEXT NOT NULL)''')

    # Commit the changes and close the database connection
    mydb.commit()
    mydb.close()

# Insert the image data into the database
def insert_image_data(query, image_data):
    # Connect to the SQLite database and create a cursor object
    mydb = sqlite3.connect('texttoimage.db')
    mycursor = mydb.cursor()

    # Insert each image into the database
    for image in image_data:
        image_url = image['largeImageURL']
        preview_url = image['previewURL']
        tags = image['tags']
        sql = "INSERT INTO images (query, image_url, preview_url, tags) VALUES (?, ?, ?, ?)"
        val = (query, image_url, preview_url, tags)
        mycursor.execute(sql, val)

    # Commit the changes and close the database connection
    mydb.commit()
    mydb.close()

# Search for images based on the query
def search_images(query):
    # Connect to the Pixabay API and retrieve the images
    response = requests.get(BASE_URL, params={
        'key': API_KEY,
        'q': query,
        'per_page': MAX_IMAGES
    }).json()

    # Check if the response contains any images
    if 'hits' in response:
        images = response['hits']
        # Insert the image data into the database
        insert_image_data(query, images)
        return images
    else:
        return []

# Check if the images exist in the database
def check_database(query):
    # Connect to the SQLite database and create a cursor object
    mydb = sqlite3.connect('texttoimage.db')
    mycursor = mydb.cursor()

    # Check if the query exists in the database
    mycursor.execute("SELECT * FROM images WHERE query=?", (query,))
    rows = mycursor.fetchall()

    # Close the database connection
    mydb.close()

    if len(rows) > 0:
        # Retrieve the image data from the database
        images = []
        for row in rows:
            image = {
                'image_url': row[2],
                'preview_url': row[3],
                'tags': row[4]
            }
            images.append(image)
        return images
    else:
        # Search for images and return the results
        return search_images(query)

# Define the main function
def main():
    # Create the database and tables if they don't exist
    create_database()

    # Start a loop to get user input and search for images
    while True:
        query = input("Enter a query to search for images (q to quit): ")
        if query == 'q':
            break

        # Check if the images exist in the database
        images = check_database(query)

        if len(images) > 0:
            # Show the images from the database
            print("Showing images from the database:")
            for image in images:
                print(image['image_url'])
        else:
            # No images found in the database, crawl and index the images
            print("No images found in the database. Crawling and indexing images...")
            images = search_images(query)
            if len(images) > 0:
                # Show the images from the API response
                print("Showing images from the API response:")
                for image in images:
                    print(image['image_url'])
            else:
                print("No images found.")

# Run the main function
if __name__ == "__main__":
    main()
