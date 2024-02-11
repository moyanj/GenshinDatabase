from pathlib import Path
from moyanlib import jsons

dird =Path('角色数据/')
for f in dird.iterdir():
    with open(f, encoding='utf-8') as i:
        info = jsons.load(i)
    with open(f'词典/Datas/{info["name"]}.txt','w', encoding='utf-8') as ff:
        profile = info['Description']
        ff.write(profile)