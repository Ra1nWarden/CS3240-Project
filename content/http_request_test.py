import requests

removedict = {'filename' : "test.txt" }
r = requests.delete("http://127.0.0.1:5000/", params=removedict)
