#!/usr/bin/env python3
"""_summary_
    This file contains functions for the github checker endpoint
"""

import requests

def check_if_event(url, last_id):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                events = response.json()
            except ValueError:
                print("Error: Response content is not valid JSON.")
                return
            i = len(events) - 1
            id = events[i]['id']
            if last_id != 0 and last_id != id: # if last id != current id, then there was a new event
                type = events[i]['type'].replace('Event', '')
                actor = events[i]['actor']['login']
                repo_name = events[i]['repo']['name']
                print(f"There was a {type} by {actor} in {repo_name}")
            return id
        else:
            print(f"Failed to fetch events at {url} :\n{response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def check_github(repo):
    """_summary_
        The endpoint allowing a user to check if there was a push in the selected repositorie.

    Returns:
        Response: _description_: The data to send back to the user as a response.
    """
    # get repo list from user, user must be able to stock repo list in db
    repo = ["https://api.github.com/repos/bazar-de-komi/terarea/events"]
    events_last_ids = [0] * len(repo)
    # token = [""] * len(repo)

    events_last_ids[0] = 1234
    for i in range(0, len(repo)):
        events_last_ids[i] = check_if_event(repo[i], events_last_ids[i])

if __name__ == '__main__':
    check_github([])

"""
keep number of events in inf loop, when there is a new event,
send the notif of what it is, even other than PushEvent
send type (without event), actor.login, and repo.name
example :
    there was a Push by HenraL in bazar-de-komi/terarea
"""
