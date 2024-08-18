import json
import hashlib

def getSHA1(text):
    sha1 = hashlib.sha1()
    sha1.update(text.encode())
    return sha1.hexdigest()[:10]

f = open("raw.txt").read()  # 读取源文件
f_list = f.splitlines()  # 分行

out = []
i = 1

for line in f_list:
    print(i)
    i += 1
    # 为空行时跳过
    if len(line) <= 3:
        continue
    # 分别解析
    content = line.split(". ")[1]
    content = content.split("——")
    # 没有作者时
    if len(content) < 2:
        content.append("未知")
    out.append({"content": content[0], "author": content[1],'id':getSHA1(content[0])})

# 保存
json.dump(out, open("Quotations.json", "w"), indent=4, ensure_ascii=False)
