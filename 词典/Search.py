from pathlib import Path
import re
import time
dir = Path('Datas/')
def is_valid_regex(pattern):
    if pattern[0] != '<':
        return False
    try:
        re.compile(pattern[1:])
        return True # 编译成功，是有效的正则表达式
    except re.error:
        return False  # 编译失败，不是有效的正则表达式

def jaccard_similarity(set1, set2):
    set1 = set(set1)
    set2 = set(set2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

def Search(search_str)
    #search_str = str(input('请输入你要查询的词（可用正则表达式，需加<）：'))
    start_time = time.time()
    regex = bool(is_valid_regex(search_str))
    matched_items = []
    analogous_items = []
    for item in dir.iterdir():
        
        if regex and re.search(search_str[1:], str(item).split('/')[1]):
            matched_items.append(item)
        elif not regex and search_str in item.name.split('.')[0]:
            matched_items.append(item)
        if not regex and jaccard_similarity(search_str,item.name.split('.')[0]) >= 0.28:
            if item not in matched_items:
                analogous_items.append(item)
    end_time = time.time()
    '''
    print(f'查找到{len(matched_items)}个词')
    if len(matched_items) > 0 or len(analogous_items) > 0:      
        ids = 1
        for i in matched_items:
            name = i.name.split('.')[0]
            print(f'{ids} ：{name}')
            ids += 1
        if len(analogous_items) > 0:
            ids = 1
            print('推荐下列相关词条：')
            for i in analogous_items[:20]:
                name = i.name.split('.')[0]
                print(f'a{ids} ：{name}')
                ids += 1
    else:
        continue
    print(end_time-start_time)
    sel = input('请输入序号：')
    if sel[0] == 'a':
        data = open(analogous_items[int(sel[1:])-1])
    else:
        data = open(matched_items[int(sel)-1])
    print()
    print(data.read())
    print()
    '''
    return 