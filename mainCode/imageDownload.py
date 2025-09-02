import requests
from constants import *

imgCount = 0
def downloadImgLocally(url):
    global imgCount
    response = requests.get(url, allow_redirects=True)

    if response.status_code == 200:
        name = f"img-{imgCount}.png"
        name = os.path.join("imgs", name)
        with open(os.path.join(OUTPUT_DIR,name), 'wb') as f:
            f.write(response.content)
        print("Pobrane")
        imgCount+=1
        return name
    else:
        print(f"Blad: {response.status_code}")
        return downloadImgLocally(url)