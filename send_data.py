import requests
import json

url = "https://striveschool-be.herokuapp.com/api/nbgrader/"

def send_json(email,ex,max_score,score):
      
  payload = json.dumps({
    "email": email,
    "exerciseId": ex,
    "numberOfExercises": max_score,
    "score": score
  })

  header = {'Content-type': "application/json"}

  response = requests.get(url, headers= header, data=payload)

  return response.text