import time, requests

    while True:
        f = requests.get("http://localhost:8000/update/")
        time.sleep(10)
