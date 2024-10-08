#!/usr/bin/env python3
"""_summary_
    This file contains functions for the github checker endpoint
"""

import requests
from fastapi import FastAPI, Response, Request
import json
import hmac
import hashlib

class Github_check:
    app = FastAPI()

    def __init__(self, repo, token = None):
        self.repo = []
        self.events_last_ids = [0] * len(repo)
        self.token = token

    def check_signature(self, body, signature):
        if self.token is None:
            return True
        secret = bytes(self.token, 'utf-8')
        expected_signature = 'sha256=' + hmac.new(secret, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_signature, signature)

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

    @app.get("/github_check")
    async def check_github(self, request: Request):
        """_summary_
            The endpoint allowing a user to check if there was a push in the selected repositorie.
        Returns:
            Response: _description_: The data to send back to the user as a response.
        """
        # get repo list from user, user must be able to stock repo list in db
        self.repo = ["https://api.github.com/repos/bazar-de-komi/terarea/events"]
        # token = [""] * len(repo)
        signature = request.headers.get('X-Hub-Signature-256')
        body = await request.body()
        if not self.check_signature(body, signature):
            return {"error": "Invalid signature"}
        while 1:
            payload = await request.json()
            repository_name = payload.get("repository", {}).get("name")
            if repository_name in self.repo:
                payload.get("ref")
        self.events_last_ids[0] = 1234

        try:
            while (1):
                for i in range(0, len(self.repo)):
                    self.events_last_ids[i] = self.check_if_event(self.repo[i], self.events_last_ids[i])
        except Exception:
            return("error in github loop")

if __name__ == '__main__':
    test = Github_check
    test.check_github([])

"""
keep number of events in inf loop, when there is a new event,
send the notif of what it is, even other than PushEvent
send type (without event), actor.login, and repo.name
example :
    there was a Push by HenraL in bazar-de-komi/terarea
"""
