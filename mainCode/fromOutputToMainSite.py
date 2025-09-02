from constants import *

with open(os.path.join(MAIN_DIR, "config.json"), 'r') as jsoner:
    data = json.load(jsoner)
    location = data["pagePath"]
    print(location)
    if os.path.exists(os.path.join(location, "imgs")):
        shutil.rmtree(os.path.join(location, "imgs"))
    shutil.copytree(os.path.join(OUTPUT_DIR, "imgs"),os.path.join(location, "imgs"))
    files = ["index.html", "main.js", "styles.css"]
    for file in files:
        if os.path.exists(os.path.join(location, file)):
            os.remove(os.path.join(location, file))
        if os.path.exists(os.path.join(OUTPUT_DIR, file)):
            shutil.copyfile(os.path.join(OUTPUT_DIR, file), os.path.join(location, file))
            os.remove(os.path.join(OUTPUT_DIR, file))