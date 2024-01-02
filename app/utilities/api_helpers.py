```python
import requests
from flask import current_app

def make_api_request(url, method='GET', headers=None, data=None, params=None):
    """
    Make an HTTP request to a given URL.
    :param url: URL to make the request to
    :param method: HTTP method to use (GET, POST, etc.)
    :param headers: HTTP headers to send with the request
    :param data: Data to send with the request (for POST, PUT, PATCH)
    :param params: URL parameters to send with the request (for GET)
    :return: Response object
    """
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=data, params=params)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, data=data, params=params)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, data=data, params=params)
        else:
            current_app.logger.error(f'Unsupported HTTP method: {method}')
            return None

        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as http_err:
        current_app.logger.error(f'HTTP error occurred: {http_err}')
    except Exception as err:
        current_app.logger.error(f'Other error occurred: {err}')
    return None
```