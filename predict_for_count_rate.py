import os
import pickle
import tensorflow as tf
from utils import create_model, get_logger
from model import Model
from loader import input_from_line
from train import FLAGS, load_config


def main(text):
    config = load_config(FLAGS.config_file)
    logger = get_logger(FLAGS.log_file)
    # limit GPU memory
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    with open(FLAGS.map_file, "rb") as f:
        tag_to_id, id_to_tag = pickle.load(f)
    with tf.Session(config=tf_config) as sess:
        model = create_model(sess, Model, FLAGS.ckpt_path, config, logger)
        sen_list = text.split("\n\n")
        e_list = []
        for index, item in enumerate(sen_list):
            line_list = item.split("\n")
            sentence = ''
            for line in line_list:
                sentence += line[0]
            result = model.evaluate_line(sess, input_from_line(sentence, FLAGS.max_seq_len, tag_to_id), id_to_tag, index)
            e_list.append(result)
    return e_list


if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    tf.app.run(main)
