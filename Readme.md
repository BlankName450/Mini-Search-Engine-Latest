# Wikipedia Search and Image Retrieval Web Application with AI Chatbot

## Overview

This Python web application is a versatile tool for searching Wikipedia articles, retrieving relevant images, performing speech-to-text conversion, and interacting with an AI chatbot. Users can communicate with the chatbot to obtain information and assistance.

![Web Application Screenshots]()
![Screenshot 2023-08-25 180120](https://github.com/BlankName450/Mini-Search-Engine-Latest/assets/62857282/0f42c8d7-b9ac-41bf-9468-964236fdf747)

![Screenshot 2023-08-25 175722](https://github.com/BlankName450/Mini-Search-Engine-Latest/assets/62857282/6ce0a47c-6ee0-4dfc-8a9a-0157e9f5b61a)

![Screenshot 2023-08-25 175746](https://github.com/BlankName450/Mini-Search-Engine-Latest/assets/62857282/22b9aa10-18cf-461d-9135-219106f26e94)

![Screenshot 2023-08-25 175734](https://github.com/BlankName450/Mini-Search-Engine-Latest/assets/62857282/3c37a88d-5dac-4214-b1dc-46841b7def8a)

![Screenshot 2023-08-25 180257](https://github.com/BlankName450/Mini-Search-Engine-Latest/assets/62857282/95d7a6af-5de6-4f9c-aa7f-763b85236e32)

![Screenshot 2023-08-25 180428](https://github.com/BlankName450/Mini-Search-Engine-Latest/assets/62857282/c9ab08a1-551c-4425-a406-cb1620d22abb)

![Screenshot 2023-08-25 180612](https://github.com/BlankName450/Mini-Search-Engine-Latest/assets/62857282/74f4ad87-76ee-40a2-bf5e-160bd0121f44)

![Screenshot 2023-08-25 180625](https://github.com/BlankName450/Mini-Search-Engine-Latest/assets/62857282/e39b6f0d-011e-4034-9b77-5ad0ffaa9861)

## Features

- **Wikipedia Article Search**: Users can search for Wikipedia articles by entering keywords in the search bar. The application retrieves relevant articles, including titles, categories, and snippets.

- **Image Search**: Users can search for images using the Pixabay API. The application displays images related to the search query along with associated tags.

- **Speech-to-Text Conversion**: The application provides a speech-to-text feature. Users can speak into their microphone, and the application converts their speech into text.

- **AI Chatbot Interaction**: Users can interact with an AI chatbot to obtain information, ask questions, and receive responses in a conversational manner.

- **Database Integration**: Data is stored and retrieved from SQLite databases. The `wikipedia.db` database contains Wikipedia article data, while the `image_search.db` database stores image search results.

- **Basic Authentication (Optional)**: The application supports basic user authentication for login and potentially signup (implementation details are not provided).

## Tools and Libraries

The following tools and libraries were used to build this application:

- Python
- HTTP Server
- SQLite Database
- Web Scraping (Beautiful Soup, Requests)
- Natural Language Processing (NLTK)
- Text Processing (TfidfVectorizer)
- Speech Recognition (SpeechRecognition)
- Wikipedia API
- Pixabay API
- AI Chatbot (OpenAI GPT-3)
- HTML Templates
- Basic Authentication (Optional)
- JSON

## Getting Started

1. Install the required Python packages:

   ```bash
   pip install speechrecognition beautifulsoup4 scikit-learn nltk openai

2. Download NLTK data: using this code lines 
      import nltk
      nltk.download('stopwords')
3.Create and set up SQLite databases: Ensure that the wikipedia.db and image_search.db databases are created and configured for data storage.
4.Run the Application write this in python compiler terminal or command prompt :
                                                                                  python start.py
5.Access the Web Application by opening a web browser and navigating to http://localhost:7112/

## Usage
Use the search bar to search for Wikipedia articles and images.
Click on the microphone icon for speech-to-text conversion.
Interact with the AI chatbot by entering text in the chat interface.

## Acknowledgments
Scikit-Learn: Scikit-Learn library for TF-IDF vectorization.
NLTK: Natural Language Toolkit for text preprocessing.
SpeechRecognition: SpeechRecognition library for speech-to-text conversion.
Pixabay API: Pixabay API for image retrieval.
OpenAI GPT-3: OpenAI GPT-3 for conversational AI capabilities.

## Contact
For questions or feedback, please contact Me @ mahmoudsamy450@gmail.com. or here. 

## LinkedIn
https://www.linkedin.com/in/mahmoud-samy-843855243/

                      
 
        
