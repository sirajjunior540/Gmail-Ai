import os
import logging
from flask import Flask, redirect, request, url_for, session, render_template
from .bot import authenticate_gmail
from .config import LOG_LEVEL, LOG_FORMAT

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    """
    Home page route.
    Displays a link to authenticate with Gmail if not already authenticated.
    """
    return render_template('index.html')

@app.route('/authenticate')
def authenticate():
    """
    Authentication route.
    Initiates the Gmail authentication flow.
    """
    try:
        # Call the authenticate_gmail function with redirect=True to get the auth URL
        auth_url = authenticate_gmail(redirect=True)
        
        # If we got a URL, redirect the user to it
        if auth_url:
            return redirect(auth_url)
        
        # If no URL is returned, authentication is already complete
        return redirect(url_for('success'))
    
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return f"Authentication error: {e}", 500

@app.route('/oauth2callback')
def oauth2callback():
    """
    OAuth callback route.
    Handles the callback from Google's OAuth service.
    """
    try:
        # Get the authorization code from the request
        code = request.args.get('code')
        
        if code:
            # Complete the authentication process with the code
            authenticate_gmail(code=code)
            return redirect(url_for('success'))
        
        error = request.args.get('error', 'Unknown error')
        logger.error(f"OAuth error: {error}")
        return f"Authentication failed: {error}", 400
    
    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        return f"OAuth callback error: {e}", 500

@app.route('/success')
def success():
    """
    Success route.
    Displayed after successful authentication.
    """
    return render_template('success.html')

def run(host='0.0.0.0', port=8080, debug=False):
    """Run the Flask application."""
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run()