import time, requests

while(True):
    f = requests.get("http://localhost:8080/update/")
    print(f.text,"\n")
    time.sleep(10)
