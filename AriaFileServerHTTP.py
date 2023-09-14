# Aria File Server HTTP Version
# HTTP File Server with Authentication
# ErfanNamira
# https://github.com/ErfanNamira/AriaFileServer

# sudo apt install python3-pip
# pip3 install flask
# python3 AriaFileServerHTTP.py

from flask import Flask, request, Response
from functools import wraps
import os

app = Flask(__name__)

# Define a dictionary to store username-password pairs (You should use a proper database in production)
users = {
    'aria': 'ariapass',
    'sara': 'sarapass',
}

# Function to check if a given username and password are valid
def is_valid_user(username, password):
    return username in users and users[username] == password

# Decorator to require authentication for specific routes
def require_auth(func):
    @wraps(func)
    def auth_wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not is_valid_user(auth.username, auth.password):
            return Response('Authentication failed', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return func(*args, **kwargs)
    return auth_wrapper

# Route for the root URL ("/") - asks for authentication
@app.route('/')
@require_auth
def index():
    # Change the welcome message here
    welcome_message = 'Welcome to the Aria File Server!'
    
    # Get the list of files in the current directory
    file_list = os.listdir('.')
    file_list_html = '<ul>'
    for filename in file_list:
        file_list_html += f'<li><a href="/files/{filename}">{filename}</a></li>'
    file_list_html += '</ul>'
    return f'{welcome_message}<br>List of files in the directory:<br>{file_list_html}'

# Simple file server route
@app.route('/files/<path:filename>')
@require_auth
def serve_file(filename):
    try:
        with open(filename, 'rb') as f:
            return Response(f.read(), mimetype='application/octet-stream')
    except FileNotFoundError:
        return 'File not found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
