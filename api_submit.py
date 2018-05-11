
# coding: utf-8

import requests

files={'files': open('submission/5.10/submit.csv','rb')}

data = {
    "user_id": "kimzenu",   #user_id is your username which can be found on the top-right corner on our website when you logged in.
    "team_token": "dda0730d880c3e82fea1be19a90335d7776403407ecdee30878f5a1c655ae53a", #your team_token.
    "description": 'naive submit use linear regression and naive factor',  #no more than 40 chars.
    "filename": "submit.csv", #your filename
}

url = 'https://biendata.com/competition/kdd_2018_submit/'

response = requests.post(url, files=files, data=data)

print(response.text)


