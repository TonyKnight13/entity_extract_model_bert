#coding:utf-8

import os
import pickle
import tensorflow as tf
from utils_law import create_model, get_logger
from model import Model
from loader import input_from_line
from train import FLAGS, load_config
from key_value import composition_key_value, characteristic_key_value


def predict(text):
    sen_list = text.split("。")
    for index, sen in enumerate(sen_list):
        sen_list[index] = sen + '。'
    config = load_config(FLAGS.config_file)
    logger = get_logger(FLAGS.log_file)
    # limit GPU memory
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    with open(FLAGS.map_file, "rb") as f:
        tag_to_id, id_to_tag = pickle.load(f)
    with tf.Session(config=tf_config) as sess:
        model = create_model(sess, Model, FLAGS.ckpt_path, config, logger)
        result_list = []
        for index, sen in enumerate(sen_list):
            result = model.evaluate_line(sess, input_from_line(sen, FLAGS.max_seq_len, tag_to_id),
                                         id_to_tag, index)
            result_list.append(result)
        # parse_result(result_list)
        print(result_list)


def parse_result(result_list):
    entity_dict_list = []
    category_list = []
    for result in result_list:
        if len(result["种类"]) > 0:
            max_entity = ""
            for category_entity in result["种类"]:
                if len(category_entity) > len(max_entity):
                    max_entity = category_entity
            if len(category_list) > 0:
                if max_entity in category_list[-1]:
                    pass
                elif category_list[-1] in max_entity:
                    category_list[-1] = max_entity
                else:
                    category_list.append(max_entity)
            else:
                category_list.append(max_entity)
    print("种类实体列表: ", category_list)

    if len(category_list) > 0:
        current_entity = category_list.pop(0)
        entity_dict_list = []
        entity_dict = {"种类": current_entity, "组分": [], "特性": [], "工艺": []}
        for result in result_list:
            if len(result["种类"]) > 0:
                max_entity = ""
                for category_entity in result["种类"]:
                    if len(category_entity) > len(max_entity):
                        max_entity = category_entity
                if max_entity == current_entity or max_entity in current_entity:
                    entity_dict = check_dict_repetition(result, entity_dict)
                else:
                    entity_dict_list.append(entity_dict)
                    current_entity = category_list.pop(0)
                    entity_dict = {"种类": current_entity, "组分": result["组分"], "特性": result["特性"], "工艺": result["工艺"]}
            else:
                check_dict_repetition(result, entity_dict)
        entity_dict_list.append(entity_dict)
        # print(entity_dict_list)
    else:
        print("该文本中没有能够抽取出钢材实体...")

    for index, entity_dict in enumerate(entity_dict_list):
        if entity_dict:
            entity_dict["组分"] = composition_key_value(entity_dict["组分"])
            entity_dict["特性"] = characteristic_key_value(entity_dict["特性"])
        entity_dict_list[index] = entity_dict

    # log(str(entity_dict_list))
    print(entity_dict_list)
    return entity_dict_list


def check_dict_repetition(origin_dict, result_dict):
    result_dict["组分"] = check_for_repetition(origin_dict["组分"], result_dict["组分"])
    result_dict["特性"] = check_for_repetition(origin_dict["特性"], result_dict["特性"])
    result_dict["工艺"] = check_for_repetition(origin_dict["工艺"], result_dict["工艺"])
    return result_dict


def check_for_repetition(origin_entity_list, result_entity_list):
    if len(origin_entity_list) > 0:
        # log(str(origin_entity_list))
        for origin_entity in origin_entity_list:
            flag = True
            if len(result_entity_list) > 0:
                for result_entity in result_entity_list:
                    if origin_entity == result_entity or origin_entity in result_entity:
                        flag = False
                if flag:
                    result_entity_list.append(origin_entity)
            else:
                result_entity_list.append(origin_entity)
    return result_entity_list


# def log(log_text):
#     path = './data/material/txt/test/log_file_test.txt'
#     with open(path, 'a', encoding='utf-8') as file:
#         file.write(log_text)
#         file.write('\n')


if __name__ == "__main__":
    text = "公诉机关昌黎县人民检察院。被告人贾某，农民。其因涉嫌掩饰、隐瞒犯罪所得罪于2014年4月17日被昌黎县公安局取保候审，2014年12月4日被昌黎县人民检察院取保候审。昌黎县人民检察院以昌检公诉刑诉（2014）379号起诉书指控被告人贾某犯掩饰、隐瞒犯罪所得罪，于2014年12月18日向本院提起公诉。本院受理后，依法适用简易程序实行独任审判，于2014年12月31日公开开庭进行了审理。昌黎县人民检察院指派代检察员赵健舒出庭支持公诉，被告人贾某到庭参加诉讼。现已审理终结。昌黎县人民检察院指控：2013年5月的一天，被告人贾某在昌黎县新集镇裴各庄一村李某（已判刑）家以3000元的价格购买了一辆大江牌150型三轮摩托车。该车由高某（已判刑）于2013年从秦皇岛市海港区盗窃所得。经昌黎县价格认证中心鉴定，该车价值人民币3000元。2013年9月29日，被告人贾某主动把车上交到公安机关，并如实向公安机关供述了自己的犯罪事实。上述事实，被告人贾某在开庭审理过程中无异议，且有昌黎县人民检察院提供的被告人贾某供述，证人高某、李某的证言，昌黎县公安局扣押清单、扣押车辆照片、户籍证明、现实表现证明、抓获经过，昌黎县价格认证中心（2014）昌价（刑）字（55）号《价格鉴证结论书》，本院（2014）昌刑初字第206号《刑事判决书》等证据证实，足以认定。本院认为，公诉机关指控被告人贾某犯罪的事实清楚，提供的证据确实、充分，对其指控的罪名成立。被告人贾某明知车辆没有合法有效的来历凭证，仍在机动车交易市场以外地点购买，主观上属明知是犯罪所得，其行为已构成掩饰、隐瞒犯罪所得罪。但案发后，被告人贾某能够主动投案，并如实供述其犯罪事实，自首情节予以认定，且收购赃车已上缴公安机关，故可对被告人贾某从轻处罚。据此，依据《中华人民共和国刑法》第三百一十二条第一款、第六十七条第一款、《最高人民法院、最高人民检察院关于办理与盗窃、抢劫、诈骗、抢夺机动车相关刑事案件具体应用法律若干问题的解释》第一条第一款第（一）项、第六条第（一）项之规定，判决如下：被告人贾某犯掩饰、隐瞒犯罪所得罪，判处罚金人民币六千元。#（罚金已缴纳）#如不服本判决，可在接到判决书的第二日起十日内，通过本院或直接向秦皇岛市中级人民法院提出上诉。书面上诉的，应交上诉状正本一份，副本三份。"
    # index = 1
    # print(sentence_predict(sentence, index))
    # test()
    predict(text)
    # list = ['0.01～1.6wt％的Fe', '0.001～0.3wt％的Cu', '0.001～0.3wt％的Mg', 'C0.16％～0.20％', 'Si0.50％～0.70％', 'C：0.14%～0.17%', 'Si：0.15%～0.35%']
    # print(composition_key_value(list))
    # log('aa')
