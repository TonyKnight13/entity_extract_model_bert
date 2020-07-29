# encoding=utf-8
import os
import pickle
import tensorflow as tf
from utils import create_model, get_logger
from model import Model
from loader import input_from_line
from train import FLAGS, load_config
from key_value import composition_key_value, characteristic_key_value


def pdf_predict():
    config = load_config(FLAGS.config_file)
    logger = get_logger(FLAGS.log_file)
    # limit GPU memory
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    with open(FLAGS.map_file, "rb") as f:
        tag_to_id, id_to_tag = pickle.load(f)
    with tf.Session(config=tf_config) as sess:
        model = create_model(sess, Model, FLAGS.ckpt_path, config, logger)
        path = "./data/material/txt/"
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".txt"):
                    print(file)
                    result_list = []
                    with open(path + file, "r", encoding="utf-8") as origin_file:
                        sen_list = origin_file.read().split("\n")
                    for index, sen in enumerate(sen_list):
                        result = model.evaluate_line(sess, input_from_line(sen, FLAGS.max_seq_len, tag_to_id),
                                                     id_to_tag, index)
                        result_list.append(result)
                        # print(result)
                    # print(result_list)
                    parse_result(result_list)


def parse_result(result_list):
    # print(result_list)
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

    log(str(entity_dict_list))
    print(entity_dict_list)


def check_dict_repetition(origin_dict, result_dict):
    result_dict["组分"] = check_for_repetition(origin_dict["组分"], result_dict["组分"])
    result_dict["特性"] = check_for_repetition(origin_dict["特性"], result_dict["特性"])
    result_dict["工艺"] = check_for_repetition(origin_dict["工艺"], result_dict["工艺"])
    return result_dict


def check_for_repetition(origin_entity_list, result_entity_list):
    if len(origin_entity_list) > 0:
        log(str(origin_entity_list))
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


def log(log_text):
    path = './data/material/txt/test/log_file_test.txt'
    with open(path, 'a', encoding='utf-8') as file:
        file.write(log_text)
        file.write('\n')


if __name__ == "__main__":
    text = "本发明涉及属于热处理领域，具体涉及一种H13钢制挤压模高温淬火工艺。H13钢(4Cr5MoSiV1)是目前国内外广泛使用的热作模具钢,其化学成分(％)为:0132～0145C,0180～1120Si,0120～0150Mn,4175～5150Cr,1110～1175Mo,0180～1120V,P≤01030,S≤01030。因其具有良好的热强性、红硬性、较高的韧性和抗热疲劳性能,故被广泛用于铝合金的热挤压模和压铸模,工作时温度可达600℃,工作条件恶劣,主要失效形式为热磨损(熔损)和热疲劳,要求表面具有高硬度、耐蚀、抗粘结等性能。H13钢常规淬火、回火后的硬度一般为42～48HRC,耐磨性不足,模具使用寿命短。鉴于模具失效大都由表面开始,从节省能源和资源,充分发挥材料性能潜力并获得特殊性能和最大经济效益出发,需要改变H13钢的热处理工艺。本发明的目的在于提供一种H13钢制挤压模高温淬火工艺，该工艺方法简单，处理后的H13钢制挤压模性能好，寿命显著增加。为了实现上述目的，本发明的技术方案如下：一种H13钢制挤压模高温淬火工艺，其特征在于，采用高温回火代替原等温退火工艺，包括如下步骤：(1)预热：在盐浴炉的600℃下保温30min，在850℃下保温30min；(2)淬火：温度为1080℃，盐浴加热20min；(3)冷却：盐浴560℃下油冷10min；(4)回火：在560℃下进行回火两次，每次2h。该发明的有益效果在于：该工艺方法简单，处理后的H13钢制挤压模性能好，寿命显著增加。"
    # index = 1
    # print(sentence_predict(sentence, index))
    # test()
    pdf_predict(text)
    # list = ['0.01～1.6wt％的Fe', '0.001～0.3wt％的Cu', '0.001～0.3wt％的Mg', 'C0.16％～0.20％', 'Si0.50％～0.70％', 'C：0.14%～0.17%', 'Si：0.15%～0.35%']
    # print(composition_key_value(list))
    # log('aa')
