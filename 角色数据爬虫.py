import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent
from moyanlib import jsons as json
from tenacity import retry,retry_if_exception_type
import os

ua = UserAgent()
headers = {"User-Agent": ua.random}
roles_r = requests.get("https://wiki.biligame.com/ys/武器一览", headers=headers)

soup = BeautifulSoup(roles_r.text, "lxml")

role_aera = soup.find("div", "resp-tab-case").find_all("div", "g")

def getTable(allrows, n,sp=True):
    cell = allrows[n].find_all("td")[0]
    try:
    	if sp:
    		return cell.text.split("\n")[0]
    	else:
    		return cell.text
    except:
    	return cell.text

def getStar(row):
	star_img = row[6].find('td').find('img')
	png = str(star_img['alt'])
	
	if png == '5星.png':
		return '5'
	else:
		return '4'
def getIMG(soupss,name):
    ff = soupss.find('img',attrs={'alt':f'{name}.png'})
    if ff:
        return ff['src']
    else:
        return None
            
def getRole(name):
    info = ""
    print('获取角色页面')
    lxz = False
    if '旅行者' in name:
        lxz = True
    role_r = requests.get("https://wiki.biligame.com/ys/" + name, headers=headers)
    role_soup = BeautifulSoup(role_r.text, "lxml")
    base_table = role_soup.find_all("table", "wikitable")[0].find("tbody")
    info_table = role_soup.find_all("table", "wikitable")[3].find("tbody")
    story_table = role_soup.find_all("table", "wikitable")[4].find("tbody")

    base_rows = base_table.find_all("tr")
    info_rows = info_table.find_all("tr")
    story_rows = story_table.find_all("tr")
    if lxz:
        photos = {
            '1':getIMG(role_soup,'旅行者立绘.png'),
            '2':getIMG(role_soup,'旅行者立绘2.png'),
            '3':getIMG(role_soup,'旅行者立绘3.png'),
            'wish':getIMG(role_soup,'旅行者抽卡立绘.png')
        }
    else:
        photos = {
            '1':getIMG(role_soup,f'{name}立绘.png'),
            '2':getIMG(role_soup,f'{name}立绘2.png'),
            'wish':getIMG(role_soup,f'{name}抽卡立绘.png' )
            
            
        }
    info = {
        "name": name,
        "title": getTable(base_rows, 0),
        "country": getTable(base_rows, 2).split("\xa0\xa0")[1],
        "profile": getTable(base_rows, 15),
        "TAG": str(getTable(base_rows, 14)).split('、'),
        "gender": getTable(base_rows, 5),
        "race": getTable(base_rows, 4),
        "element": getTable(base_rows, 8).split("元素")[0],
        "type": getTable(base_rows, 7),
        "constellation": getTable(base_rows, 11),
        "weapon": getTable(base_rows, 9).split("武器使用")[0],
        "nicknames": str(getTable(info_rows, 0)).split('、'),
        "job": getTable(info_rows, 2),
        "CV": getTable(info_rows, 3),
        "birthday" : getTable(info_rows, 7),
        "stories" : {
        	'pron': getTable(story_rows,1),
        	'1': getTable(story_rows,3),
        	'2': getTable(story_rows,5),
        	'3': getTable(story_rows,7),
        	'4': getTable(story_rows,9),
        	'5': getTable(story_rows,11),
        	'things': getTable(story_rows,13),
        	'eye': getTable(story_rows,15),
        },
        'photos':photos,
        
        'star': getStar(base_rows)
    }
    
    print()
    # time.sleep(random.uniform(0,3))
    json.dump(info,open(f'Datas/{name.replace("/","_")}.json','w'),toacill=False,indent=4)
    return info

roles = {}

for role in role_aera:
    role_name = role.find("div", "L").text
    print(role_name)
    if "旅行者" in role_name:
        path = role_name.split('(')[1].split(')')[0]
        if not os.path.exists(f'Datas/旅行者_{path}.json'):
            role_info = getRole('旅行者/'+path)
    elif "派蒙" in role_name:
        continue
    else:
        if not os.path.exists(f'Datas/{role_name}.json'):
            role_info = getRole(role_name)
            roles[role_name] = role_info
        
json.dump(roles,open('AllData.json','w'),toacill=False,indent=4)