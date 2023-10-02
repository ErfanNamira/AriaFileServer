# Aria File Server HTTPS Version
# v. 1.1
# HTTPS File Server with Authentication
# ErfanNamira
# https://github.com/ErfanNamira/AriaFileServer

# sudo apt update
# sudo apt install certbot python3-pip python3-certbot-nginx python3-flask
# pip3 install flask passlib Werkzeug Flask-Caching
# sudo certbot --nginx -d sub.domain.com
# sudo ufw allow 443/tcp
# sudo python3 AriaFileServerHTTPS.py

from flask import Flask, request, Response, send_file
from functools import wraps
import os
import mimetypes
from passlib.hash import bcrypt
from werkzeug.exceptions import NotFound
from werkzeug.utils import secure_filename
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  # Simple in-memory caching, you can choose other caching methods as needed

# Define a dictionary to store username-password pairs with hashed passwords
users = {
    'aria': bcrypt.using(rounds=13).hash('your_password'),  # Replace 'your_password' with the actual password
}

# Function to verify a given username and password
def is_valid_user(username, password):
    if username in users:
        return bcrypt.verify(password, users[username])  # Verify the hashed password
    return False

# Decorator to require authentication for specific routes
def require_auth(func):
    @wraps(func)
    def auth_wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not is_valid_user(auth.username, auth.password):
            return Response('Authentication failed', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return func(*args, **kwargs)
    return auth_wrapper

# Set CORS headers for all routes
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    return response

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
@cache.cached(timeout=300)  # Cache the file response for 5 minutes (adjust timeout as needed)
def serve_file(subpath):
    requested_path = os.path.join('.', subpath)
    
    if os.path.exists(requested_path):
        try:
            mime_type, _ = mimetypes.guess_type(requested_path)
            if mime_type:
                return send_file(requested_path, as_attachment=True, mimetype=mime_type, conditional=True)
            else:
                return send_file(requested_path, as_attachment=True, conditional=True)
        except Exception as e:
            app.logger.error(f"Error serving file '{subpath}': {e}")
            return 'Error serving the file', 500
    else:
        raise NotFound(description=f"The requested resource '{subpath}' was not found on this server.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2083, debug=True, ssl_context=('path_to_your_cert_file.pem', 'path_to_your_key_file.pem'))
