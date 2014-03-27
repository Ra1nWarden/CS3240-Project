import requests

myfiles = {'file': open('test.txt', 'rw')}

r = requests.post("http://127.0.0.1:5000/", files=myfiles)
print r.text
