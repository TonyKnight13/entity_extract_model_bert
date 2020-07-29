# coding=utf-8
import os
import re
import pymysql


def text_preprocess(text):
    symbol_dict = {" ": "", "\n": "", "(": "（", ",": "，", ";": "；"}
    for key, value in symbol_dict.items():
        text = text.replace(key, value)
    return text


# 将网上复制粘贴的句子中的空格、多余的换行去掉
def origin_data_process():
    origin_path = "./data/cailiao_test_sentence.txt"
    with open(origin_path, "r", encoding="utf-8") as origin_file:
        text = origin_file.read()
    sen_list = text.split("\n")
    data_path = "./data/material_data.txt"
    with open(data_path, "a", encoding="utf-8") as data_file:
        for sen in sen_list:
            sen = sen.replace("\n", "").replace(" ", "")
            data_file.write(sen + "\n")


# 将句子转换为“字 O”的待标注格式
def tag_process(origin_path, data_path):
    with open(origin_path, "r", encoding="utf-8") as origin_file:
        text = origin_file.read()
    text = text.replace(" ", "").replace(" ", "").replace("\n", "")
    sen_list = text.split("。")
    if "" in sen_list:
        sen_list.remove("")
    for i in range(0, len(sen_list)):
        sen_list[i] = sen_list[i] + "。"
    with open(data_path, "w", encoding="utf-8") as data_file:
        for sen in sen_list:
            for word in sen:
                data_file.write(word + " O" + "\n")
            data_file.write("\n")


# 自动标注列表中的实体
def auto_mark(path, entity_list, flag):
    mark = ""
    if flag == "1":
        mark = "PER"
    elif flag == "2":
        mark = "ORG"
    elif flag == "3":
        mark = "MIS"
    elif flag == "4":
        mark = "ARM"
    elif flag == "5":
        mark = "BAS"
    elif flag == "6":
        mark = "AIR"
    elif flag == "7":
        mark = "POR"
    elif flag == "8":
        mark = "NAT"
    elif flag == "9":
        mark = "LOC"

    length = len(entity_list)
    for i in range(0, length):
        for j in range(i + 1, length):
            if len(entity_list[j]) > len(entity_list[i]):
                temp = entity_list[i]
                entity_list[i] = entity_list[j]
                entity_list[j] = temp

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


def get():
    connection = pymysql.connect(host="localhost", user="root", passwd="123456", db="cailiao_knowledgegraph")
    cursor = connection.cursor()
    sql = '''select id, shuru_wenben from input_material_task'''
    cursor.execute(sql)
    text_tuple = cursor.fetchall()
    for text in text_tuple:
        path = './data/material/txt/' + str(text[0]) + ".txt"
        with open(path, "w", encoding='utf-8') as file:
            file.write(text[1])


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


def daObiaoqian():
    for root, dirs, files in os.walk("./data/material/txt/"):
        for file in files:
            if file.endswith(".txt"):
                new_file = './data/material/txt/test' + file
                file = './data/material/txt/' + file
                tag_process(file, new_file)


def pingjie_test_data():
    test_data_path = "./data/material/count_rate_data.txt"
    for root, dirs, files in os.walk("./data/material/txt/"):
        for file in files:
            if file.endswith(".txt"):
                origin_file_path = "./data/material/txt/" + file
                origin_file = open(origin_file_path, "r", encoding="utf-8")
                text = origin_file.read().replace("\n\n。 O", "").replace(" O\n。 O\n\n\n", "")
                text = text.replace("\n\n\n", "\n\n")
                text = text.replace("  O\n", "").replace("  I-CAT\n", "").replace("  I-COM\n", ""). \
                    replace("  I-CAR\n", "").replace("  I-CHA\n", "").replace("  O\n", "")
                test_data = open(test_data_path, "a", encoding="utf-8")
                test_data.write(text)


def qukongge():
    path = "./data/material/count_rate_data.txt"
    with open(path, "r", encoding="utf-8") as file:
        # text = file.read().replace("  O\n", "").replace("  I-CAT\n", "").replace("  I-COM\n", ""). \
        #     replace("  I-CAR\n", "").replace("  I-CHA\n", "").replace("  O\n", "")
        text = file.read().replace("\n\n", "\n")
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def chongzhiweiO(input_path,output_path):

    with open(input_path, "r", encoding="utf-8") as file:
        text = file.read()
    text = text.replace("B-PER", "O").replace("I-PER", "O").replace("B-ORG", "O").replace("I-ORG", "O")\
        .replace("B-MIS", "O") .replace("I-MIS", "O").replace("B-ARM", "O").replace("I-ARM", "O").\
        replace("B-LOC", "O").replace("I-LOC", "O").replace("B-POR", "O").replace("I-POR", "O").\
        replace("B-AIR", "O").replace("I-AIR", "O").replace("B-NAT", "O").replace("I-NAT", "O").\
        replace("B-BAS", "O").replace("I-BAS", "O").replace("B-", "O").replace("I-", "O")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)


if __name__ == "__main__":
    # chongzhiweiO("data/test_all_O.txt", "data/test_all.txt")
    # chongzhiweiO("data/1111.txt")
    # tag_process("data/test_all_sentence.txt", "data/test_all_O.txt")
    # tag_process("data/lujun_sentence.txt", "data/lujun_train.txt")
    dabiaoqian("data/peizhi.txt", "data/train_all.txt")
    # dabiaoqian("data/peizhi.txt", "data/1111.txt")
    # with open("test_all_O.txt", 'r', encoding='utf-8') as f:
    #     test_data = f.read()
    # test_data = test_data.replace("\n O\n", "\n")
    # with open("test_all_O.txt", 'w', encoding='utf-8') as f2:
    #     f2.write(test_data)
