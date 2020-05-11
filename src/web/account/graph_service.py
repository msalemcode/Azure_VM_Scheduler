import requests

class GraphService:

    def __init__(self, access_token):
        self.access_token = access_token
    
    def get_me(self):
        return self._get_json('/me')

    def _get_json(self, url):
        response = requests.get(
            'https://graph.microsoft.com/v1.0' + url, 
            headers = {
                'Authorization': 
                'Bearer ' + self.access_token
            })
        return response.json()