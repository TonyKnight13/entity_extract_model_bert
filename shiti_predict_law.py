# coding=utf-8
#@Time: 2020/7/3 18:22
#@Auther:zhaorui
#@File: shiti_predict.py

import os
import pickle
import tensorflow as tf
from utils_law import create_model, get_logger
from model import Model
from loader import input_from_line
from train import FLAGS, load_config
from law_tool import auto_mark
import json

def shiti_predict(text_path,output_path):
    config = load_config(FLAGS.config_file)
    logger = get_logger(FLAGS.log_file)
    # limit GPU memory
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    with open(FLAGS.map_file, "rb") as f:
        tag_to_id, id_to_tag = pickle.load(f)
    sess = tf.Session(config=tf_config)
    model = create_model(sess, Model, FLAGS.ckpt_path, config, logger)

    with open(text_path, "r", encoding='utf-8') as f:
        text = f.read()
        json_str = json.loads(text)
        print(json_str)

    output_file = open(output_path, 'w', encoding='utf-8')
    result_list = []
    for i in json_str:
        index = i["id"]
        text = i["判决书"]
    # sen_list = text.split("\n")
    # sen_list = text.split("。")
    # if "" in sen_list:
    #     sen_list.remove("")
    # result_list = []
    # for index, sen in enumerate(sen_list):
    #     sen_list[index] = sen + '。'
    # for index, sen in enumerate(sen_list):
        result = model.evaluate_line(sess, input_from_line(text, FLAGS.max_seq_len, tag_to_id),id_to_tag, index)
        output_file.write(json.dumps(result, ensure_ascii=False))
        output_file.write("\n")
        result_list.append(result)
    print(result_list)
    return result_list


def reverse_dabiaoqian(entity_list, sentence_path, result_path):
    ship_all_list = []
    plane_all_list = []
    missile_all_list = []
    army_all_list = []
    location_all_list = []
    port_all_list = []
    airport_all_list = []
    base_all_list = []
    nature_all_list = []

    for entity_dict in entity_list:

        clerk_list = entity_dict["书记员"]
        judge_list = entity_dict["审判员"]
        chief_judge_list = entity_dict["审判长"]
        prosecutor_list = entity_dict["检察员"]
        defendant_list = entity_dict["被告人"]
        victim_list = entity_dict["被害人"]
        witness_list = entity_dict["证人"]
        counsel_list = entity_dict["辩护人"]
        juror_list = entity_dict["陪审员"]
        others_list = entity_dict["其他"]

        for ship in clerk_list:
            if ship not in ship_all_list:
                ship_all_list.append(ship)
        for plane in judge_list:
            if plane not in plane_all_list:
                plane_all_list.append(plane)
        for missile in chief_judge_list:
            if missile not in missile_all_list:
                missile_all_list.append(missile)
        for army in prosecutor_list:
            if army not in army_all_list:
                army_all_list.append(army)
        for location in defendant_list:
            if location not in location_all_list:
                location_all_list.append(location)
        for port in victim_list:
            if port not in port_all_list:
                port_all_list.append(port)
        for airport in counsel_list:
            if airport not in airport_all_list:
                airport_all_list.append(airport)
        for base in juror_list:
            if base not in base_all_list:
                base_all_list.append(base)
        for nature in others_list:
            if nature not in nature_all_list:
                nature_all_list.append(nature)

    tag_process(sentence_path, result_path)
    auto_mark(result_path, ship_all_list, "1")
    auto_mark(result_path, plane_all_list, "2")
    auto_mark(result_path, missile_all_list, "3")
    auto_mark(result_path, army_all_list, "4")
    auto_mark(result_path, base_all_list, "5")
    auto_mark(result_path, airport_all_list, "6")
    auto_mark(result_path, port_all_list, "7")
    auto_mark(result_path, nature_all_list, "8")
    auto_mark(result_path, location_all_list, "9")


def tag_process(origin_path, data_path):
    with open(origin_path, "r", encoding="utf-8") as origin_file:
        text = origin_file.read()
    text = text.replace(" ", "").replace(" ", "")
    sen_list = text.split("\n")
    # for i in range(0, len(sen_list)):
    #     sen_list[i] = sen_list[i] + "。"
    with open(data_path, "w", encoding="utf-8") as data_file:
        for sen in sen_list:
            for word in sen:
                data_file.write(word + " O" + "\n")
            data_file.write("\n")


def ziO_trans_sentence(input_path,output_path):
    with open(output_path, "w", encoding="utf-8") as f_out:
        with open(input_path, "r", encoding="utf-8") as f:
            for row in f.readlines():
                if row == "\n":
                    f_out.write("\n")
                else:
                    f_out.write(row[0])


if __name__ == '__main__':
    # os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    # tf.app.run(main)
    #text = "近日,美国航空界有传言说,美国空军正在评估采购F-15X。这是已有45年历史的F-15鹰式战机的最新升级型号。文章称,五角大楼准备向国会提交采购F-15X战机的预算案,并且计划与波音公司签订采购合同。如果这项采购成功推进,那么F-15X可能成为美国空军自2001年以来采购的首款新式非隐形战斗机。\n福特号航空母舰造价达约130亿美元，是美国海军有史以来造价最高的一艘舰船。"
    #text = "福特号航空母舰造价达约130亿美元，是美国海军有史以来造价最高的一艘舰船。"
    # new_text = ""
    # for i in range(0,len(text)):
    #     new_text += text[i] + " O" + "\n"
    # print(new_text)
    # with open("junshi_data/test_all_sentence.txt", 'r', encoding='utf-8') as f:
    #     test_data = f.read()
    # shiti_predict(test_data)
    # entity_list = shiti_predict(test_data)
    # reverse_dabiaoqian(entity_list, "junshi_data/test.txt", "junshi_data/result.txt")
    # tag_process("test.txt", "result.txt")
    # ziO_trans_sentence("data\junshi\junshishiti_data_test_total.txt","data\junshi\junshishiti_test_total_sentence.txt")


    shiti_predict("新判决书2.json", "新判决书2标注结果.json")