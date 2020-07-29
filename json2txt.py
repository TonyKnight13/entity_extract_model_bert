import pandas as pd
import re


def trans2txt(file):
    with open(file, 'r',encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r'u3000',"",text)
    text = re.sub('[a-zA-Z]{10,}.*/[/|]$',"",text)
    text = re.sub('\(u200b.+?\)',"",text)
    text = re.sub('[a-mo-zA-Z][a-zA-Z\d=+]{20,}/{1,2}',"",text)
    text = re.sub('CONTROLiSignatureOffice\.SignatureCtrl\\\\s',"",text)
    
    # df = pd.read_json(text)
    # df.to_json('新判决书.json', orient="records", lines=True, force_ascii=False)

    file_name = "1.json"
    # 以写入的方式打开
    f = open(file_name,'w', encoding="utf-8")
    # 写入内容
    f.write(text)
    # 换行符

    # 关闭文件
    f.close()

    # df = df.iloc[:,2]
    # df.to_csv('判决书.txt', header=None, index=False, encoding = "utf-8")

if __name__ == '__main__':
    trans2txt('判决书.json')