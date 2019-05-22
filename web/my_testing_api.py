import requests

# URL_BASE = 'http://localhost:5000/'
URL_BASE = 'http://localhost:8000/'
auth = ('patkennedy79@yahoo.com', 'password1234')

# API v1.2 - Get Authentication Token
print('Retrieving authentication token...')
url = URL_BASE + 'get-auth-token'
r = requests.get(url, auth=auth)
print(r.status_code)
print(r.headers)
auth_request = r.json()
token_auth = (auth_request['token'], 'unused')

# API v1.2 - GET (All)
print('Retrieving all recipes...')
url = URL_BASE + 'api/v1_2/recipes'
r = requests.get(url, auth=token_auth)
print(r.status_code)
print(r.text)

# API v1.2 - PUT (Metadata)
print('Updating recipe #2...')
url = URL_BASE + 'api/v1_2/recipes/2'
json_data = {'title': 'Updated recipe', 'description': 'My favorite recipe'}
r = requests.put(url, json=json_data, auth=token_auth)
print(r.status_code)
print(r.text)

# API v1.2 - PUT (Add image)
print('Updating recipe #2 with recipe image IMG_6127.JPG')
url = URL_BASE + 'api/v1_2/recipes/2'
# r = requests.put(url, auth=token_auth, files={'recipe_image': open('IMG_6127.JPG', 'rb')})
r = requests.put(url, auth=token_auth, files={'recipe_image': open('./project/tests/IMG_6127.JPG', 'rb')})

print(r.status_code)
print(r.text)

