import http.server
import socketserver
import urllib.parse
import json
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained model and tokenizer
model_name = 'gpt2-medium'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Set model to evaluation mode
model.eval()

# Define the name of the chatbot
bot_name = "Seekfy"

# Set the pad token ID to eos token ID
model.config.pad_token_id = model.config.eos_token_id

# Function to generate an answer given a question
def generate_answer(question):
    # Tokenize the question
    input_ids = tokenizer.encode(question, return_tensors='pt')
    attention_mask = torch.ones_like(input_ids)

    # Generate answer
    with torch.no_grad():
        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=100,
            num_return_sequences=1,
            temperature=0.8,  # Adjust the temperature for controlling randomness
        )

    # Decode and return the answer
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

# Handler for incoming requests
class MyHandler(http.server.SimpleHTTPRequestHandler):
    # Override the do_GET method to handle the request
    def do_GET(self):
        # Parse the query string to extract the question parameter
        query = urllib.parse.urlparse(self.path).query
        query_components = urllib.parse.parse_qs(query)
        question = query_components.get('question', [''])[0]

        # Generate an answer to the question
        if question:
            # Check if user asked about the bot's name
            if any(keyword in question.lower() for keyword in ["your name", "who are you", "what should I call you"]):
                answer = f"You can call me {bot_name}."
            # Check if user asked about the bot's creator
            elif any(keyword in question.lower() for keyword in ["your creator", "who made you", "who created you","who create you" , "who designed you" ,"what is the name of your developer" , "your developer" , "your programmer" , "who developed you" , "Mohamed ehab" , "seekfy creator", "seekfy developer", "seekfy programmer", "seekfy designer"]):
                answer = f"His name is Mohamed Ehab or (S h a d o w), also known as the godfather of programmers."
            # Check if the user provided valid input
            elif not question.strip():
                answer = "Please ask a valid question."
            else:
                # Generate the answer
                answer = generate_answer(question)

            # Set response headers and write the response body
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
            self.send_header('Access-Control-Allow-Methods', 'GET')
            self.end_headers()
            response = {'answer': answer}
            response_json = json.dumps(response)
            self.wfile.write(response_json.encode())
        else:
            # If no question parameter was provided, serve the HTML file
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('smartsearch.html', 'rb') as file:
                self.wfile.write(file.read())

# Set up the web server
with socketserver.TCPServer(("", 8000), MyHandler) as httpd:
    print("Serving at port", 8000)
    httpd.serve_forever()
