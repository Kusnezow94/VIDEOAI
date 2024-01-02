```python
import os
import requests
from flask import url_for, session, current_app
from oauthlib.oauth2 import WebApplicationClient

# Initialize OAuth client with client ID and secret from environment variables
google_client_id = os.environ.get("GOOGLE_CLIENT_ID")
google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
google_discovery_url = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(google_client_id)

def get_google_provider_cfg():
    return requests.get(google_discovery_url).json()

def get_google_auth_url():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for('auth_views.google_login_callback', _external=True),
        scope=["openid", "email", "profile", "https://www.googleapis.com/auth/youtube.readonly"],
    )
    return request_uri

def get_google_token(code):
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(google_client_id, google_client_secret),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    return token_response.json()

def get_google_userinfo():
    google_provider_cfg = get_google_provider_cfg()
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    return unique_id, users_email, users_name, picture

def get_channel_details():
    access_token = session.get("access_token")
    if not access_token:
        return "Access token is missing.", 400

    youtube_endpoint = "https://www.googleapis.com/youtube/v3/channels"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    params = {
        "part": "snippet,contentDetails,statistics",
        "mine": "true",
    }
    response = requests.get(youtube_endpoint, headers=headers, params=params)

    if response.status_code != 200:
        return "Failed to retrieve channel details.", 400

    channel_data = response.json().get("items", [])[0]
    channel_name = channel_data["snippet"]["title"]
    channel_description = channel_data["snippet"]["description"]

    return channel_name, channel_description
```