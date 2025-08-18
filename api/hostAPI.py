import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask, redirect, request, session
from google_auth_oauthlib.flow import Flow
import os


# Flask app for GoogleAPI Web.
app = Flask(__name__)
app.secret_key = "super_secret_key"

# Create flow from client-secrets.
flow = Flow.from_client_secrets_file(
    client_secrets_file = "credentials.json",
    scopes = ["https://www.googleapis.com/auth/calendar.readonly"],
    redirect_uri = "https://infamously-busy-sandpiper.cloudpub.ru/oauth2callback"
)

# Google auch URL
url = flow.authorization_url(
        access_type="offline"
)

# Write to file for broadcast the bot.
with open("url.txt", "w") as f:
    f.write(str(url))
    print(url)

# Index Page
@app.route("/")
def index():
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )
    session["state"] = state
    return redirect(authorization_url)

# Redirect Page (Google Auch)
@app.route("/oauth2callback")
def oauth2callback():
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials

    return f"""
    <h2>Успешный вход!</h2>
    <p>Access token: {credentials.token}</p>
    <p>Refresh token: {credentials.refresh_token}</p>
    """
# Run
if __name__ == "__main__":
    app.run(port=8080)
