from pathlib import Path
import re
import time

dataDir = Path('Datas/')

def is_valid_regex(pattern):
    
    if pattern[0] != '<':
        return False
    try:
        re.compile(pattern[1:])
        return True # 编译成功，是有效的正则表达式
    except re.error:
        return False  # 编译失败，不是有效的正则表达式

def jaccardSim(set1, set2):
    
    set1 = set(set1)
    set2 = set(set2)
    
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    return len(intersection) / len(union)

def Search(search_str):
    
    #search_str = str(input('请输入你要查询的词（可用正则表达式，需加<）：'))
    startTime = time.time_ns()
    
    regex = bool(is_valid_regex(search_str))
    print('正则查询：', regex)
    matched_items = []
    analogous_items = []
    
    for item in dataDir.iterdir():
        
        if regex and re.search(search_str[1:], str(item).split('/')[1]):
            # 正则表达式搜索
            matched_items.append(item)
            continue
            
        elif not regex and search_str in item.name.split('.')[0]:
            # item名称搜索
            matched_items.append(item)
            continue
            
        if not regex and jaccardSim(search_str,item.name.split('.')[0]) >= 0.28:
            # 推荐搜索
            if item not in matched_items:
                analogous_items.append(item)
                
    end_time = time.time_ns()
    
    print('用时:',(end_time - startTime)/1000, 'μs')
    
    return matched_items, analogous_items
if __name__ == '__main__' :   
    while True:
        instr = input('请输入你要查询的词（可用正则表达式，需加<）：')
        matched ,analogous = Search(instr)
        print(f'查找到{len(matched)}个词')
        if len(matched) > 0 or len(analogous) > 0:      
            ids = 1
            print('0 : 取消')
            for i in matched:
                name = i.name.split('.')[0]
                print(f'{ids} ：{name}')
                ids += 1
            if len(analogous) > 0:
                ids = 1
                print('推荐下列相关词条：')
                for i in analogous[:20]:
                    name = i.name.split('.')[0]
                    print(f'a{ids} ：{name}')
                    ids += 1
        else:
            continue
        
        sel = input('请输入序号：')
        if sel[0] == 'a':
            data = open(analogous[int(sel[1:])-1])
        elif sel == '0':
            continue
        else:
            data = open(matched[int(sel)-1])
        print()
        print(data.read())
        print()
        