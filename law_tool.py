# coding=utf-8
import os
import re

# def transtxt(origin_path, data_path):
#     masks =   ['被告人', '辩护人', '检察员', '被害人', '证人', '审判长',
#              '陪审员', '书记员', '审判员', '其他'];

#     with open(origin_path, 'r', encoding='utf-8') as file:
#         text = file.read()
#         people_list = text.split("\n\n")
#         for i in range(0,len(people_list)):
#             entity_list = people_list[i].split("\n")

# 将网上复制粘贴的句子中的空格、多余的换行去掉
def origin_data_process():
    origin_path = "判决书.txt"
    with open(origin_path, "r", encoding="utf-8") as origin_file:
        text = origin_file.read()
    sen_list = text.split("\n")
    data_path = "新判决书.txt"
    with open(data_path, "a", encoding="utf-8") as data_file:

        for sen in sen_list:
            sen = sen.replace("\n", "").replace(" ", "").replace("\t", "")
            
        j = 0 
        for i in range(len(sen_list)):
            if sen_list[j] == "":
                sen_list.pop(j)
            else:
                j += 1

        for sen in sen_list:
            data_file.write(sen + "\n")

  
# 句子切割(。为尾的句成段，段以\n区分)
def cutinsen(origin_path, data_path):
    with open(origin_path, "r", encoding="utf-8") as origin_file:
        text = origin_file.read()
    sen_list = text.split("\n")
    with open(data_path, "a", encoding="utf-8") as data_file:
        for sen in sen_list:
            if "。" in sen:
                sen_listinlist = sen.split("。")
                if "" in sen_listinlist:
                    sen_listinlist.remove("")
                for sl in sen_listinlist:
                    sl += "。"
                    data_file.write(sl + "\n")
            else:
                data_file.write(sen + "\n")


# 将句子转换为“字 O”的待标注格式
def tag_process(origin_path, data_path):
    with open(origin_path, "r", encoding="utf-8") as origin_file:
        text = origin_file.read()
    sen_list = text.split("\n")
    with open(data_path, "w", encoding="utf-8") as data_file:
        for sen in sen_list:
            for word in sen:
                data_file.write(word + " O" + "\n")
            data_file.write("\n")

# origin_path即包含所有已标注实体的txt
def transtxt(origin_path, peizhi_list, data_path):
    masks = ['被告人', '辩护人', '检察员', '被害人', '证人', '审判长',
             '陪审员', '书记员', '审判员', '其他']

    with open(origin_path, 'r', encoding='utf-8') as file:
        mark_dict = {}
        text = file.read()
        people_list = text.split("\n\n")
        for i in range(0, len(people_list)):
            entity_list = people_list[i].split("\n")
            # v=''
            # for m in masks:
            #     v = re.match(m,entity_list[0])
            #     if v!=None:
            #         break
            mark_dict[peizhi_list[i]] = entity_list
            for key, value in mark_dict.items():

                auto_mark(data_path, value, key)


# 自动标注列表中的实体
def auto_mark(path, entity_list, flag):
    mark = ""
    if flag == "0":
        mark = "clerk"
    elif flag == "1":
        mark = "judge"
    elif flag == "2":
        mark = "chief_judge"
    elif flag == "3":
        mark = "prosecutor"
    elif flag == "4":
        mark = "defendant"
    elif flag == "5":
        mark = "victim"
    elif flag == "6":
        mark = "witness"
    elif flag == "7":
        mark = "counsel"
    elif flag == "8":
        mark = "juror"
    elif flag == "9":
        mark = "others"

    length = len(entity_list)
    # for i in range(0, length):
    #     for j in range(i + 1, length):
    #         if len(entity_list[j]) > len(entity_list[i]):
    #             temp = entity_list[i]
    #             entity_list[i] = entity_list[j]
    #             entity_list[j] = temp

    with open(path, "r", encoding="utf-8") as file_read:
        text = file_read.read()
    for entity in entity_list:
        entity_origin = ""
        entity_mark = ""
        for i in range(0, len(entity)):
            entity_origin = entity_origin + entity[i] + " O\n"
            if i == 0:
                entity_mark = entity[i] + " B-" + mark + "\n"
            else:
                entity_mark = entity_mark + entity[i] + " I-" + mark + "\n"
        # print(entity_origin)
        # print(entity_mark)
        if entity_origin in text:
            text = text.replace(entity_origin, entity_mark)
    with open(path, "w", encoding="utf-8") as file_write:
        file_write.write(text)


# 生成配置列表
def derivePL(origin_path):
    peizhi_list = []
    with open(origin_path, 'r', encoding='utf-8') as file:
        text = file.read()
        peizhi = text.split("\n\n")
        for i in range(0, len(peizhi)):
            peizhi_list_temp = peizhi[i].split("\n")
            peizhi_list.append(peizhi_list_temp.pop(0))
    return peizhi_list


if __name__ == "__main__":
    
    # origin_data_process()
    # cutinsen('新判决书.txt','新判决书1.txt')
    tag_process('新判决书1.txt','cut判决书.txt')

    peizhi_list = derivePL('peizhi.txt')
    transtxt('people_list.txt', peizhi_list, 'cut判决书.txt')


def dabiaoqian(peizhi_path, data_path):
    with open(peizhi_path, 'r', encoding='utf-8') as file:
        mark_dict = {}
        text = file.read().replace(" ", "").replace(" ", "")
        peizhi_list = text.split("\n\n")
        for i in range(0, len(peizhi_list)):
            entity_list = peizhi_list[i].split("\n")
            entity_list.pop(0)
            mark_dict[peizhi_list[i][0]] = entity_list
    print(mark_dict)
    # for count in range(233, 401):
    #     path = './data/material/txt/test' + str(count) + '.txt'
    #     # print(temp_list)
    #     for key, value in mark_dict.items():
    #         print(key)
    #         auto_mark(path, value, key)

    for key, value in mark_dict.items():
        # print(key)
        auto_mark(data_path, value, key)

