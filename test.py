import requests
import json

url = "https://striveschool-be.herokuapp.com/api/nbgrader/"

payload = json.dumps({
  "email": "jonperezetxebarria@gmail.com",
  "exerciseId": "0",
  "numberOfExercises": 0,
  "score": 0
})


response = requests.post( url, data=payload)

print(response.text)