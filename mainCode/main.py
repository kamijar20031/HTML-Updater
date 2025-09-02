from datetime import datetime
from imageDownload import *

htmlData = ""

with open(os.path.join(TEMPLATE_DIR, "index.html"), 'r') as html:
    htmlData = html.read()

class TimeRow:
    def __init__(self, year):
        self.year = year
    
    def getCode(self):
        return f"<div class='yearRow'><div>{self.year}</div><div>{self.year}</div></div>\n"
    
class Project:
    def __init__(self, name, langs, images, url, id, description):
        self.name = name
        self.langs = langs
        self.images = images
        self.url = url
        self.id = id
        self.description = description
    def getCode(self):
        return f"<div class='project'><img id='images_{self.id}' onclick='changeIMG({self.id})' src='{self.images[0]}'><div class='projectTitle'><a href='{self.url}' target='_blank'>{self.name}</a><p>{" ".join(self.langs)}</p>{self.description}<p></p></div></div>\n"

data = ""
with open(os.path.join(TEMPLATE_DIR, SETTINGS_FILE)) as json_data:
    data = json_data.read()

memory = ""
with open(os.path.join(OUTPUT_DIR, MEM_FILE)) as json_data:
    memory = json_data.read()

conf = ""
with open(os.path.join(MAIN_DIR, CONFIG)) as json_data:
    conf = json_data.read()

memConf = ""
with open(os.path.join(OUTPUT_DIR, MEM_CONFIG)) as json_data:
    memConf = json_data.read()

if data!=memory and conf!=memConf:
    with open(os.path.join(OUTPUT_DIR, MEM_FILE), 'w') as output:
        output.write(data)
    with open(os.path.join(OUTPUT_DIR, MEM_CONFIG), 'w') as output:
        output.write(conf)
    data = json.loads(data)
    conf = json.loads(conf)
    repos = []
    def sorter(el):
        confs = conf["projectData"]
        for exc in confs:
            if el["name"]==exc["name"]:
                for sets in exc.keys():
                    el[sets] = exc[sets]
                break
        return datetime.strptime((el["createdAt"]), "%Y-%m-%dT%H:%M:%SZ")
    data.sort(key=sorter)

    divs = []
    crntDate =""
    javascript = "const images = ["
    id = 0
    if os.path.exists(os.path.join(OUTPUT_DIR, "imgs")):
        shutil.rmtree(os.path.join(OUTPUT_DIR, "imgs"))
    os.makedirs(os.path.join(OUTPUT_DIR, "imgs"))
    for repo in data:
        repo["createdAt"] = repo["createdAt"][:4]
        if crntDate!= repo["createdAt"]:
            crntDate= repo["createdAt"]
            divs.append(TimeRow(crntDate))
        if repo["images"] != "":
            repo["images"] = repo["images"].split("\n")
            imgs = []
            for i in range(len(repo["images"])):
                repo["images"][i] = downloadImgLocally(repo["images"][i])
            inside = f"{repo["images"]}"
            javascript += "{srcs:" + inside + ", idx:0},\n"
            
        else:
            javascript += "{srcs: [], idx:0},\n"
            repo["images"] = ["none"]
        repo["name"] = repo["name"].replace("-", " ")
        numLang = len(repo["languages"])
        if not isinstance(repo["languages"][0], str):
            repo["languages"] = [lang["node"]["name"] for lang in repo["languages"]]
        if numLang>3:
            repo["languages"] = repo["languages"][:3]
        divs.append(Project(repo["name"], repo["languages"], repo["images"], repo["url"], id, repo["description"]))
        id+=1
    javascript+="];\n"
    ""
    projectCode = ""
    for div in divs:
        projectCode += div.getCode()
    htmlData = htmlData.replace("{PROJECT DATA}", projectCode)

    files = ["main.js", "styles.css"]
    for file in files:
        pathToFile = os.path.join(OUTPUT_DIR, file)
        pathCopy = os.path.join(TEMPLATE_DIR, file)
        if os.path.isfile(pathToFile):
            os.remove(pathToFile)
        shutil.copyfile(pathCopy, pathToFile)

   
    with open(os.path.join(OUTPUT_DIR, "main.js"), "r") as jsIN:
        javascript += jsIN.read()
    with open(os.path.join(OUTPUT_DIR, "main.js"), "w") as jsOUT:
        jsOUT.write(javascript)

    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as output:
        output.write(htmlData)
else:
    print("Brak zmian!")