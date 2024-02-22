"""
This module provides functions for downloading data from the Concept2 Log API.

Functions:
- get_page: Get the next page of results and save it to a file.
- get_page2: Get the next page of results and save it to a file.
- get_results: Get the results for all users in the database and save them to a file.
- get_stroke_data: Get the stroke data for a specific result and save it to a file.
- get_age: Get the age of a user.
"""

import concurrent.futures
from json import dump
from datetime import datetime, timedelta

from requests import get

from database_request import get_list_user_ids as glui

API_ROOT = "https://log.concept2.com"

access_tokens = {}
refresh_tokens = {}


def get_page(next_page, headers, user_id, output):
    """Get the next page of results and save it to a file."""
    res = get(next_page, headers=headers, timeout=10)
    outfile = f'{output}/{str(user_id)}.json'
    with open(outfile, "w", encoding="utf-8") as f:
        dump(res.json(), f, indent=4)



def get_results(api_token, days):
    """Get the results for all users in the database and save them to a file."""
    date = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    headers = {"Authorization": f"Bearer {api_token}"}
    users = glui()

    def fetch_and_update(user):
        endpoint = f"{API_ROOT}/api/users/{user}/results?from={date}"
        get_page(endpoint, headers, user, 'json')
        print(f"User ID {user} updated successfully.")

    # Use a ThreadPoolExecutor to run `fetch_and_update` in multiple threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(fetch_and_update, users)

    # Wait for all threads to complete
    executor.shutdown(wait=True)


def get_stroke_data(user_id, result_id, api_token):
    """Get the stroke data for a specific result and save it to a file."""
    headers = {"Authorization": f"Bearer {api_token}"}
    endpoint = f"{API_ROOT}/api/users/{user_id}/results/{result_id}/strokes"
    get_page(endpoint, headers, result_id, 'strokes')


def get_age(user_id, api_token):
    """Get the age of a user."""
    headers = {
        "Authorization": "Bearer " + str(api_token),
    }

    response = get(API_ROOT + "/api/users/" + str(user_id), headers=headers, timeout=10)

    data = response.json()
    dob = data["data"].get(
        "dob"
    )  # access 'dob' from the 'data' dictionary within 'data'
    dob = datetime.strptime(str(dob), "%Y-%m-%d")
    now = datetime.now()
    age = now.year - dob.year
    if (now.month, now.day) < (dob.month, dob.day):
        age -= 1
    return age
