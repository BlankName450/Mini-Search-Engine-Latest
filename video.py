from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pytube import Search
from bs4 import BeautifulSoup
import requests
import json

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('video.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def do_POST(self):
        if self.path == '/search':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            query = parse_qs(post_data.decode('utf-8'))['query'][0]
            search_results = Search(query)
            video_data = []
            for video in search_results.results:
                title = video.title
                description = video.description
                video_url = f"https://www.youtube.com/watch?v={video.video_id}"
                try:
                    thumbnail_url = video.thumbnail_url
                except AttributeError:
                    thumbnail_url = get_thumbnail_url(video.video_id)
                video_data.append({'title': title, 'description': description, 'thumbnail_url': thumbnail_url, 'video_url': video_url})
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(video_data).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def get_thumbnail_url(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    thumbnail_url = soup.find('meta', property='og:image')['content']
    return thumbnail_url

if __name__ == '__main__':
    server_address = ('', 8002)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Server running on port 8002')
    httpd.serve_forever()