import pandas as pd
import re


def unRepeated(path, new_path):
    data = pd.read_table(path, header=None, encoding='utf-8', sep='\n')
    data1 = data.iloc[:, 0]

    dlist = data1.values.tolist()
    new_l = list(set(dlist))
    new_l.sort()

    df = pd.DataFrame(new_l)
    df.to_csv(new_path, header=None, index=False, encoding="utf-8")


def removePunctuation(path, new_path):
    masks = ['被告人', '辩护人', '检察员', '被害人', '证人', '审判长',
             '人民陪审员', '书记员', '代理审判员', '代理检察员', '受害单位', '委托诉讼代理人']
    data = pd.read_table(path, header=None, encoding='utf-8', sep='\n')
    data1 = data.iloc[:, 0]
    dlist = data1.values.tolist()
    new_l = list(set(dlist))
    
    for i in new_l:
        result = re.search('、',i)


if __name__ == "__main__":
    unRepeated('主要人物实体（9大类+其他）.txt','people_list.txt')