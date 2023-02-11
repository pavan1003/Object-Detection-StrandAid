import requests

url = "https://comikstorm.pythonanywhere.com/objects"

payload={'data': '''{
    "imageBy": 5,
    "lat": 25,
    "long": 69,
    "object": "tree",
    "time": "October 8, 2022 at 4:28:27 AM UTC+5:30"
}'''}
files=[
  ('file',('shubham.jpg',open('E:\\shubham.jpg','rb'),'image/jpeg'))
]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)