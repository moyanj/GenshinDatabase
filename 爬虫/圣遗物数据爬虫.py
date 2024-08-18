import requests
from bs4 import BeautifulSoup
from moyanlib import jsons

roles_r = requests.get("https://wiki.biligame.com/ys/圣遗物一览")

soup = BeautifulSoup(roles_r.text, "lxml")


def GetRole(name):
    print("获取角色页面")
    role_r = requests.get("https://wiki.biligame.com/ys/" + name)
    role_soup = BeautifulSoup(role_r.text, "lxml")
    storise = []
    #print(role_soup.find_all('div','story'))
    for i in role_soup.find_all('div','story'):
        storise.append(i.text)
    ret = {
        "name": name,
        "story": storise,
        "TAG": role_soup.find('div','tag').text.split('：')[1].split('、'),
    }
    jsons.dump_f(ret, "../圣遗物数据/" + name + ".json", indent=4, toacill=False)
    return ret


role_aera = soup.find("div", "resp-tab-case").find_all("div", "g")
for role in role_aera:
    role_name = role.find("div", "L").text
    print(role_name)
    GetRole(role_name)
