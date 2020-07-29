import pdfplumber
import os
import re


def pdf_to_sen_list(file_dir):
    save_path = "./data/material/txt/"
    name_compile = re.compile("发明名称(.*).{4}摘要")
    summary_compile = re.compile("摘要(.*)")
    claims_pattern_list = [re.compile("[一二三四五六七八九十]、"), re.compile(r"\d{1,2}）")]
    instructions_pattern = re.compile(r"\[\d{4}\]")
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if file.endswith(".pdf"):
                summary_sen_list = []  # 摘要的句子列表
                summary = ""
                claims_sen_list = []  # 权利要求书句子列表
                claims = ""
                instructions_sen_list = []  # 说明书句子列表
                instructions = ""
                index = 0
                name = "未找到专利名"
                with pdfplumber.open(file_dir + file) as pdf:
                    for page in pdf.pages:
                        index += 1
                        text = page.extract_text()
                        text = text_preprocess(text)
                        # print(text)
                        if index == 1:
                            try:
                                name = re.findall(name_compile, text)[0]
                                print(name)
                                if len(name) > 20:
                                    name = name[0:21]
                                if "/" in name:
                                    name = name.replace("/", "或")
                            except:
                                pass
                            # 摘要
                            summary = re.findall(summary_compile, text)[0]
                        if text[0:5] == "权利要求书":
                            text = text.split("页", 1)[1]
                            text = text[0:-2]  # 去除页码
                            claims += text
                        if text[0:3] == "说明书":
                            text = text.split("页", 1)[1]
                            text = text[0:-2]
                            instructions += text
                summary_sen_list = summary.split("。")
                print(summary_sen_list)

                claims_sen_list_temp = claims.split("。")
                for pattern in claims_pattern_list:
                    for sen in claims_sen_list_temp:
                        for item in claims_sen_list:
                            if sen in item:
                                claims_sen_list.remove(item)
                        if re.findall(pattern, sen):
                            for spl_sen in re.split(pattern, sen):
                                claims_sen_list.append(spl_sen)
                        else:
                            claims_sen_list.append(sen)
                print(claims_sen_list)

                instructions_sen_list_temp = instructions.split("。")
                for sen in instructions_sen_list_temp:
                    for item in instructions_sen_list:
                        if sen in item:
                            instructions_sen_list.remove(item)
                    if re.search(instructions_pattern, sen):
                        for spl_sen in re.split(instructions_pattern, sen):
                            instructions_sen_list.append(spl_sen)
                    else:
                        instructions_sen_list.append(sen)
                print(instructions_sen_list)

                with open(save_path + name + ".txt", "a") as txt_file:
                    txt_file.write("摘要\n")
                    for sen in summary_sen_list:
                        if sen:
                            if sen.endswith("；") or sen.endswith("："):
                                sen = sen[0:-1]
                            txt_file.write(sen + "。\n")
                    txt_file.write("权利要求书\n")
                    for sen in claims_sen_list:
                        if sen:
                            if sen.endswith("；") or sen.endswith("："):
                                sen = sen[0:-1]
                            txt_file.write(sen + "。\n")
                    txt_file.write("说明书\n")
                    for sen in instructions_sen_list:
                        if sen:
                            if sen.endswith("；") or sen.endswith("："):
                                sen = sen[0:-1]
                            txt_file.write(sen + "。\n")


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


# 讲句子转换为“字 O”的待标注格式
def tag_process():
    origin_path = "./data/material_data.txt"
    with open(origin_path, "r", encoding="utf-8") as origin_file:
        text = origin_file.read()
    sen_list = text.split("\n")
    data_path = "./data/train_data.txt"
    with open(data_path, "a", encoding="utf-8") as data_file:
        for sen in sen_list:
            for word in sen:
                data_file.write(word + " O" + "\n")
            data_file.write("\n")


if __name__ == "__main__":
    # origin_data_process()
    # tag_process()
    pdf_to_sen_list("./data/material/")
    # text_list = ["[0004]为实现上述目的，本发明包括如下技术方案：[0005]一种Ti5Mo5V6Cr3Al钛合金厚壁管加工方法，该方法包括如下步骤：[0006]一、按以下比例配料：Mo：4.5wt％～5.7wt％；V：4.5wt％～5.7wt％；Cr：5.5～6.5wt％；Al：2.5～3.5wt％；Fe＜0.30wt％；C：＜0.05wt％N：＜0.04wt％；H：＜0.015wt％；O：＜0.15wt％；余量为钛；[0007]二、将配料压制成电极，在真空自耗电炉中经2～3次熔炼成铸锭300-500；[0008]三、1050～1150℃经锻造、轧制获得所需尺寸的棒材；[0009]四、棒材经机加工获得待轧管坯；[0010]五、待轧管坯在800～1000℃经斜轧穿孔获得9～11mm壁厚的厚壁管；[0011]六、经450～650℃保温1～8小时真空时效处理；[0012]七、性能检测及压力试验，合格后，成品"]
    # pattern = re.compile(r"\[\d{4}\]")
    # for sen in text_list:
    #     print(sen)
    #     if re.search(pattern, sen):
    #         temp_sen = sen
    #         temp_list = re.split(pattern, temp_sen)
    #         for item in temp_list:
    #             text_list.append(item)
    #         text_list.remove(sen)
    # print(text_list)
