import requests

endpoint = "http://localhost:8000/api/"

# Sends HTTP Request to the endpoint URL and returns the Response
get_response = requests.get(endpoint, params={"abc": 123}, json={"query": "Hello Ayush"})

# Prints the response as text which is an HTML source code
# print(get_response.text)
# print(get_response.status_code)

print(get_response.json())