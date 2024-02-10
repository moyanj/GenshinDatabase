import requests
from bs4 import BeautifulSoup
from moyanlib import jsons
roles_r = requests.get("https://wiki.biligame.com/ys/武器一览")

soup = BeautifulSoup(roles_r.text, "lxml")
def getRole(name):
    info = ""
    print('获取角色页面')
    role_r = requests.get("https://wiki.biligame.com/ys/" + name)
    role_soup = BeautifulSoup(role_r.text, "lxml")
    role_data = role_soup.find_all('div','card-content3')
    ret = {
        'name':name,
        'profile':role_data[0].text,
        'type':role_data[2].text,
        'TAG':role_data[3].text.split('、')
    }
    jsons.dump_f(ret,'武器数据/'+name+'.json',indent=4, toacill=False)
    return ret
role_aera = soup.find("div", "resp-tab-case").find_all("div", "g")
for role in role_aera:
    role_name = role.find("div", "L").text
    print(role_name)
    getRole(role_name)