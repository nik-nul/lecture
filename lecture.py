import requests
import datetime
import json
import dateutil.parser


today = datetime.date.today()

NAME = ["HEAD1", "HEAD2", "MID", "TAIL", "lecH", "lecM"]

for name in NAME:
    with open(name, "r") as text:
        exec(f"{name} = text.read()")

def kerning(name, res="", remaining=14):
    if remaining <= 0 or name == "":
        return res + ("..." if name else "")
    first = name[0]
    if first >= 'A' and first <= 'z':
        remaining -= 1
    else:
        remaining -= 2
    return kerning(name[1:], res+first, remaining)

def sub(a, b):
    res = []
    names = [entry["title"] for entry in b]
    for entry in a:
        if not (entry["title"] in names):
            res.append(entry)
    return res


def inter(a, b):
    res = []
    names = [entry["title"] for entry in b]
    for entry in a:
        if entry["title"] in names:
            res.append(entry)
    return res


data = requests.get("https://lecture.idealclover.cn/lecture/getPending").json()

with open("pending.json")as f:
    old = json.load(f)

new = sub(data, old)

for entry in new:
    entry['publish'] = today.__str__()

now = new + inter(old, data)

with open("pending.json", 'w')as f:
    json.dump(now, f)

TABLE = ""

now = sorted(now, key=lambda s: dateutil.parser.parse(s["date"]))

for entry in now:
    TABLE += f"《{kerning(entry['title'])}》 & {entry['date'].replace('-', '.')[5:]} & {entry['publish'].replace('-', '.')[5:]} \\\\\n"

CONTENT= ""

for entry in new:
    CONTENT += "\\section{" + entry["title"] + "}\n" +\
        "主讲人：" + entry["teacher"] + "\\\\" +\
        "时间：" + entry["date"] + entry["startTime"] + "\\\\" +\
        "地点：" + entry["classroom"] + "\\\\" +\
        "简介：" + entry["info"].replace("\n", "\\\\") + "\\\\" +\
        (entry["special"] + "\\\\" if entry["special"] != "无" else "") +\
        (entry["other"] + "\\\\" if entry["other"] != "无" else "") + '\n'

res = HEAD1 + today.__str__() + HEAD2 + TABLE + MID + CONTENT + TAIL

with open("lec.tex", 'w') as f:
    f.write(res)

resn = lecH + TABLE + lecM + CONTENT.replace("section", "subsection")

with open("news.tex", 'w') as f:
    f.write(resn)