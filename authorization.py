"""
This module provides functions for authentication and authorization in the C2_Scraper project.

Functions:
- read_refresh_token(): Read the refresh token from a file.
- write_refresh_token(refresh_token): Write the refresh token to a file.
- quick_auth(): Quickly authenticate the user and return the URL of the new page.
- authorize(): Authorize the user and return the authorization code.
- exchange(auth_code): Exchange the authorization code for an access token.
- refresh(refresh_token): Refresh the access token using the refresh token.
- auth(): Catchall authentication.
"""
from os import chmod, makedirs
from os.path import exists
from datetime import datetime, timedelta

from requests import post
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

API_ROOT = "https://log.concept2.com"
REDIRECT_URI = "insert_redirect_uri_here"
SCOPE = "user:read,results:read"
CLIENT_ID = "hidden"  # "hidden" for security reasons
CLIENT_SECRET = "hidden"  # "hidden" for security reasons
AUTH_URL = f"{API_ROOT}/oauth/authorize?client_id={CLIENT_ID}&scope={SCOPE}&response_type=code&redirect_uri={REDIRECT_URI}"
TOKEN_URL = "https://log.concept2.com/oauth/access_token"
EMAIL = "insert_email_here"
USERNAME = "insert_username_here"
PASSWORD = "insert_password_here"



date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
access_tokens = {}
refresh_tokens = {}


def read_refresh_token():
    """Read the refresh token from a file."""
    path = "data/refresh_token.txt"
    chmod(path, 0o777)
    with open(path, "r", encoding="utf-8") as f:
        refresh_token = f.read()
    return refresh_token


def write_refresh_token(refresh_token):
    """Write the refresh token to a file."""
    path = "data/refresh_token.txt"
    if not exists("data"):
        makedirs("data")
    chmod(path, 0o777)
    with open(path, "w", encoding="utf-8") as f:
        f.write(refresh_token)


def quick_auth():
    """Quickly authenticate the user and return the URL of the new page."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options = webdriver.ChromeOptions()
    options.page_load_strategy = "eager"

    driver = webdriver.Chrome(options=options)
    new_url = None
    try:
        driver.get(AUTH_URL)

        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys(USERNAME)
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(PASSWORD)

        submit = driver.find_element(By.CLASS_NAME, "btn-primary")
        submit.click()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-success"))
        )

        button = driver.find_element(By.NAME, "approve")
        button.click()

        new_url = driver.current_url

    finally:
        driver.quit()
    return new_url


def authorize():
    """Authorize the user and return the authorization code."""
    url = quick_auth()
    authorisation = url.split("=")[1]
    print(authorisation)
    return authorisation


def exchange(auth_code):
    """Exchange the authorization code for an access token."""
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }
    response = post(TOKEN_URL, data=data, timeout=20)
    if response.status_code == 200:
        api_token = response.json()["access_token"]
        refresh_token = response.json()["refresh_token"]
        print(api_token)
        print(refresh_token)
        write_refresh_token(refresh_token)
        return api_token, refresh_token
    else:
        print(f"Failed to retrieve access token 2. Status code: {response.status_code}")
        return None, None


def refresh(refresh_token):
    """Refresh the access token using the refresh token."""
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "user:read",
    }

    # Make the POST request
    response = post(TOKEN_URL, data=data, timeout=20)

    # If the request was successful, extract the access token
    if response.status_code == 200:
        access_tokens[EMAIL] = response.json()["access_token"]
        refresh_tokens[EMAIL] = response.json()["refresh_token"]
        print(access_tokens[EMAIL])
        print(refresh_tokens[EMAIL])
        write_refresh_token(refresh_tokens[EMAIL])
        return access_tokens[EMAIL], refresh_tokens[EMAIL]
    else:
        print(f"Failed to retrieve access token 2. Status code: {response.status_code}")
        return None, None


def auth():
    """Catchall authentification"""
    auth_token = authorize()
    api_token, _ = exchange(auth_token)  # refresh_token
    return api_token
