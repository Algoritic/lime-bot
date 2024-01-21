import requests
import json
from decouple import config

class MPulseSessionManager:
    def __init__(self, username, password, base_url=config("LIMESURVEY_BASE_URL")):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.username = username
        self.password = password

    def get_session_key(self):
        self.url = f"{self.base_url}/index.php/admin/remotecontrol"
        payload = json.dumps({
            "method": "get_session_key",
            "params": [self.username, self.password],
            "id": 1
        })

        response = requests.post(self.url, headers=self.headers, data=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Extract the "result" value (session key) and return it
            return data.get("result")
        else:
            # If the request was not successful, return None or raise an exception
            return None
