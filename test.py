import requests
import json

url = "https://striveschool-be.herokuapp.com/api/nbgrader/"

payload = json.dumps({
  "email": "jonperezetxebarria@gmail.com",
  "exerciseId": "0",
  "numberOfExercises": 0,
  "score": 0
})

header = {'Content-type': "application/json"}

response = requests.post( url, headers= header, data=payload)

print(response.text)