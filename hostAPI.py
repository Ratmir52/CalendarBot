import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask, redirect, request, session
from google_auth_oauthlib.flow import Flow
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"  # нужно для session

# создаем flow
flow = Flow.from_client_secrets_file(
    "credentials.json",
    scopes=["https://www.googleapis.com/auth/calendar.readonly"],
    redirect_uri="http://localhost:8080/oauth2callback"
)



@app.route("/")
def index():
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )
    session["state"] = state
    return redirect(authorization_url)

@app.route("/oauth2callback")
def oauth2callback():
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials

    credentials.from_authorized_user_file("token.json", "https://www.googleapis.com/auth/calendar.readonly")
    return f"""
    <h2>Успешный вход!</h2>
    <p>Access token: {credentials.token}</p>
    """

if __name__ == "__main__":
    app.run(port=8080, debug=True)
