import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent
from moyanlib import jsons as json
import os

ua = UserAgent()
headers = {"User-Agent": ua.random}
roles_r = requests.get("https://wiki.biligame.com/ys/角色", headers=headers)

soup = BeautifulSoup(roles_r.text, "lxml")

role_aera = soup.find("div", "resp-tab-case").find_all("div", "g")


def getTable(allrows, n, sp=True):
    cell = allrows[n].find_all("td")[0]
    try:
        if sp:
            return cell.text.split("\n")[0]
        else:
            return cell.text
    except Exception:
        return cell.text


def getStar(row):
    star_img = row[6].find("td").find("img")
    png = str(star_img["alt"])

    if png == "5星.png":
        return "5"
    else:
        return "4"


def getIMG(soupss, name):
    ff = soupss.find("img", attrs={"alt": f"{name}"})
    if ff:
        return ff["src"]
    else:
        return None


def getRole(name):
    info = ""
    print("获取角色页面")
    lxz = False
    if "旅行者" in name:
        lxz = True
    role_r = requests.get("https://wiki.biligame.com/ys/" + name, headers=headers)
    role_soup = BeautifulSoup(role_r.text, "lxml")
    print(role_soup.find('div', 'thumb', 'tright'))
    base_table = role_soup.find_all("table", "wikitable")[0].find("tbody")
    info_table = role_soup.find_all("table", "wikitable")[3].find("tbody")
    story_table = role_soup.find_all("table", "wikitable")[4].find("tbody")

    base_rows = base_table.find_all("tr")
    info_rows = info_table.find_all("tr")
    story_rows = story_table.find_all("tr")
    if lxz:
        photos = {
            "1": getIMG(role_soup, "旅行者立绘.png"),
            "2": getIMG(role_soup, "旅行者立绘2.png"),
            "3": getIMG(role_soup, "旅行者立绘3.png"),
            "wish": getIMG(role_soup, "旅行者抽卡立绘.png"),
        }
    else:
        photos = {
            "1": getIMG(role_soup, f"{name}立绘.png"),
            "2": getIMG(role_soup, f"{name}立绘2.png"),
            "wish": getIMG(role_soup, f"{name}抽卡立绘.png"),
        }
    info = {
        "Name": name,
        "Designation": getTable(base_rows, 0),
        'Fullname': getTable(base_rows, 1),
        "Birthday": getTable(info_rows, 6),
        "Weapon": getTable(base_rows, 9).split("武器使用")[0],
        "Country": getTable(base_rows, 2).split("\xa0\xa0")[1],
        "Description": getTable(base_rows, 15),
        "Gender": getTable(base_rows, 5),
        "Race": getTable(base_rows, 4),
        "Star": getStar(base_rows),
        "Vision": getTable(base_rows, 8).split("元素")[0],
        "Type": getTable(base_rows, 7),
        "Constellation": getTable(base_rows, 11),
        'ActualInstallationTime':getTable(base_rows, 13),
        "Job": getTable(info_rows, 2),
        "Nicknames": str(getTable(info_rows, 0)).split("、"),
        "TAG": str(getTable(base_rows, 14)).split("、"),
        "Photos": photos,
        "CV": {
            'Chinese':getTable(info_rows, 3),
            'Japanese':getTable(info_rows, 4),
            'Korean':getTable(info_rows, 5),
            'English':getTable(info_rows,6)
        },
        "Stories": {
            "Pron": getTable(story_rows, 1),
            "1": getTable(story_rows, 3),
            "2": getTable(story_rows, 5),
            "3": getTable(story_rows, 7),
            "4": getTable(story_rows, 9),
            "5": getTable(story_rows, 11),
            "Things": getTable(story_rows, 13),
            "Vision": getTable(story_rows, 13),
        },
    }
    # time.sleep(random.uniform(0,3))
    json.dump(
        info, open(f'../角色数据/{name.replace("/","_")}.json', "w"), toacill=False, indent=4
    )
    return info


roles = {}

for role in role_aera:
    role_name = role.find("div", "L").text
    print(role_name)
    if "旅行者" in role_name:
        '''
        path = role_name.split("(")[1].split(")")[0]
        if not os.path.exists(f"角色数据/旅行者_{path}.json"):
            role_info = getRole("旅行者/" + path)
        '''
        continue
    elif "派蒙" in role_name:
        continue
    else:
        if not os.path.exists(f"../角色数据/{role_name}.json"):
            role_info = getRole(role_name)
            roles[role_name] = role_info

json.dump(roles, open("../角色数据/AllData.json", "w"), toacill=False, indent=4)
