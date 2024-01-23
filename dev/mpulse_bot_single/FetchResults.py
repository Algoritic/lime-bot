import requests
import json
from MpulseSessionManager import MPulseSessionManager
import base64

class Process:
    @staticmethod
    def decode_base64_from_dict(data, type='csv', name='test'):
        try:
            # Extracting the base64 encoded result
            encoded_result = data.get("result")
            if not encoded_result:
                return "No 'result' field found in the provided data."

            # Decoding the base64 encoded string
            if type == 'csv':
                decoded_result = base64.b64decode(encoded_result).decode('utf-8')
                with open(f'{name}.csv', 'w', encoding='utf-8') as file:  # Note 'w' instead of 'wb'
                    file.write(decoded_result)
            elif type == 'pdf':  # Note the use of elif for better structure
                decoded_result = base64.b64decode(encoded_result)
                with open(f'{name}.pdf', 'wb') as file:
                    file.write(decoded_result)
            return decoded_result
        except Exception as e:
            return f"An error occurred during decoding: {e}"
        
class MPulseAPI:
    def __init__(self, base_url="https://mpulse.maybanksandbox.com"):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json'
        }

    def make_request(self, method, params):
        url = f"{self.base_url}/index.php/admin/remotecontrol"
        payload = json.dumps({
            "method": method,
            "params": params,
            "id": 1
        })

        response = requests.post(url, headers=self.headers, data=payload)

        return response
