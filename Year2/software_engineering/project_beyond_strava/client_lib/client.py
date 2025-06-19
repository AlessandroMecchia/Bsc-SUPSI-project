import requests
from .config import BASE_URL
from .exception import ApiException, NetworkError

class APIClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint):
        url = f"{self.base_url}/{endpoint}"

        try:
            response = self.session.get(url)
        except requests.RequestException as e:
            raise NetworkError(e)

        if not response.ok:
            raise ApiException(response.status_code, response.text)

        try:
            return response.json()
        except ValueError:
            raise ApiException(response.status_code, "JSON not valid")

    def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"

        try:
            response = self.session.post(url, json=data)
        except requests.RequestException as e:
            raise NetworkError(e)

        if not response.ok:
            raise ApiException(response.status_code, response.text)

        try:
            return response.json()
        except ValueError:
            raise ApiException(response.status_code, "JSON not valid")

    def put(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.put(url, json=data)
        except requests.RequestException as e:
            raise NetworkError(e)
        if not response.ok:
            raise ApiException(response.status_code, response.text)
        try:
            return response.json()
        except ValueError:
            raise ApiException(response.status_code, "JSON not valid")

    def delete(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.delete(url)
        except requests.RequestException as e:
            raise NetworkError(e)
        if not response.ok:
            raise ApiException(response.status_code, response.text)
        try:
            return response.json()
        except ValueError:
            raise ApiException(response.status_code, "JSON not valid")