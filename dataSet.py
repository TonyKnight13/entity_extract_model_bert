import os
import random


def deriveDS(o_path, train, dev, test):
    with open(o_path, "rt", encoding="utf-8") as origin_file:
        text = origin_file.read()
    sen_list = text.split("\n")
    l = len(sen_list)
    pos = int(l*.7)
    pos2 = int(l*.9)

    parts = sen_list[:pos], sen_list[pos:pos2], sen_list[pos2:]
    with open(train, "a", encoding="utf-8") as data_file:
        for sen in parts[0]:
            data_file.write(sen + "\n")
    with open(dev, "a", encoding="utf-8") as data_file:
        for sen in parts[1]:
            data_file.write(sen + "\n")
    with open(test, "a", encoding="utf-8") as data_file:
        for sen in parts[2]:
            data_file.write(sen + "\n")

if __name__ == "__main__":
    deriveDS('cut判决书.txt','train.txt','dev.txt','test.txt')