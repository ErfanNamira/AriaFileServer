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
    
    # Get the list of files and directories in the current directory
    items = os.listdir('.')
    item_list_html = '<ul>'
    for item in items:
        item_path = os.path.join('.', item)
        item_list_html += f'<li><a href="/files/{item_path}">{item}</a></li>'
    item_list_html += '</ul>'
    return f'{welcome_message}<br>List of files and directories in the current directory:<br>{item_list_html}'

# Simple file server route
@app.route('/files/<path:subpath>')
@require_auth
def serve_file(subpath):
    # Construct the full path to the requested resource
    requested_path = os.path.join('.', subpath)

    if os.path.exists(requested_path):
        if os.path.isfile(requested_path):
            # If it's a file, serve it
            try:
                with open(requested_path, 'rb') as f:
                    return Response(f.read(), mimetype='application/octet-stream')
            except FileNotFoundError:
                return 'File not found', 404
        elif os.path.isdir(requested_path):
            # If it's a directory, list its contents
            items = os.listdir(requested_path)
            item_list_html = '<ul>'
            for item in items:
                item_path = os.path.join(subpath, item)
                item_list_html += f'<li><a href="/files/{item_path}">{item}</a></li>'
            item_list_html += '</ul>'
            return f'Contents of directory {subpath}:<br>{item_list_html}'
        else:
            return 'Not a file or directory', 400  # Handle other types of resources
    else:
        return 'Resource not found', 404  # Return a 404 if the resource doesn't exist

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2082, debug=True)
