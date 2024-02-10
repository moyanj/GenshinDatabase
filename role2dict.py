from pathlib import Path
from moyanlib import jsons

dird =Path('武器数据/')
for f in dird.iterdir():
    info = jsons.load(open(f))
    ff = open(f'词典/Datas/{info["name"]}.txt','w')
    ff.write(info['profile'])