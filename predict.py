#coding:utf-8

import os
import pickle
import tensorflow as tf
from utils_law import create_model, get_logger
from model import Model
from loader import input_from_line
from train import FLAGS, load_config


def predict(text):
    config = load_config(FLAGS.config_file)
    logger = get_logger(FLAGS.log_file)
    # limit GPU memory
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    with open(FLAGS.map_file, "rb") as f:
        tag_to_id, id_to_tag = pickle.load(f)
    with tf.Session(config=tf_config) as sess:
        model = create_model(sess, Model, FLAGS.ckpt_path, config, logger)
        sen_list = text.split("。")
        e_list = []
        for index, item in enumerate(sen_list):
            line_list = item.split("\n")
            sentence = ''
            for line in line_list:
                sentence += line[0]
            result = model.evaluate_line(sess, input_from_line(sentence, FLAGS.max_seq_len, tag_to_id), id_to_tag, index)
            e_list.append(result)
    return e_list

def main(_):
    predict('公诉机关河北省昌黎县人民检察院。#被告人王某，农民。2014年10月15日因涉嫌交通肇事罪被河北省昌黎县公安局刑事拘留，2014年10月24日经河北省昌黎县公安局取保候审，2014年12月10日被河北省昌黎县人民检察院取保候审。昌黎县人民检察院以昌检公诉刑诉（2014）384号起诉书指控被告人王某犯交通肇事罪，于2014年12月18日向本院提起公诉。本院受理后，依法适用简易程序，实行独任审判，于2014年12月22日公开开庭审理了本案。昌黎县人民检察院指派检察员张立敏出庭支持公诉，被告人王某到庭参加诉讼。现已审理终结。昌黎县人民检察院指控：2014年10月15日5时许，被告人王某驾驶冀B×××××（冀B×××××挂）号重型半挂牵引车，沿205国道昌黎县东外环由南向北行驶至海宝海鲜加工场路段时，与同向行驶的奚悦驾驶的无号牌三轮摩托车相撞，造成奚悦当场死亡、双方车辆损坏的交通事故。经昌黎县交警大队道路交通事故认定书认定，被告人王某负此事故的主要责任。案发后，双方就民事赔偿问题已达成赔偿协议，被告人王某取得被害人家属的谅解。#案发后，被告人王某打电话报警并在现场等候，民警到现场后将其传唤到交警大队进行询问，王某如实供述了自己的犯罪事实。#上述事实，被告人王某在开庭审理中未提出异议，并有公诉机关提供的受案登记表，证人张某、奚某证言，昌黎县公安局道路交通事故认定书、昌黎县公安局道路交通事故尸体检验鉴定书及被告人王某供述与辩解、户籍证明、现实表现说明、抓获经过等证据证实，足以认定。本院认为，昌黎县人民检察院指控被告人王某犯罪的事实清楚，证据确实、充分，故对其指控的罪名成立。被告人王某违反我国交通运输管理法规，驾驶机动车发生交通事故致一人死亡，且负此事故的主要责任，其行为已构成交通肇事罪。但被告人王某有自首情节，已赔偿了被害人亲属的经济损失，得到谅解。综合上述情节，可对被告人王某从轻处罚。故依据《中华人民共和国刑法》第一百三十三条、第六十七条第一款、第七十二条第一款之规定，判决如下：被告人王某犯交通肇事罪，判处有期徒刑一年，缓刑一年。#（缓刑考验期限，从判决确定之日起计算。）#如不服本判决，可在接到判决书的第二日起十日内，通过本院或直接向秦皇岛市中级人民法院提出上诉。书面上诉的，应交上诉状正本一份，副本三份。')


if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    tf.app.run(main)
