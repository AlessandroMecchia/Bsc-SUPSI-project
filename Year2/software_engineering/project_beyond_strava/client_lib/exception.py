class ApiException(Exception):
    def __init__(self, status_code, text):
        super().__init__(f"API ERROR: {status_code}: {text}")
        self._status_code = status_code
        self._text = text
        
    @property
    def status_code(self):
        return self._status_code

class NetworkError(Exception):
    def __init__(self, text):
        super().__init__(f"Network Error: {text}")



