import threading
import requests
def run(url):
    while True:
        try:
            response = requests.get(url)
            print(response.status_code)
        except:
            pass
for i in range(1): threading.Thread(target=run, args=('https://www.ekwing.com',)).start()
