import re

element_type_dict1 = {'C': '碳', 'N': '氮', 'O': '氧', 'F': '氟', 'B': '硼', 'P': '磷', 'S': '硫', 'K': '钾', 'V': '钒',
                      'Y': '钇', 'I': '碘', 'W': '钨', 'U': '铀'}

element_type_dict2 = {'He': '氦', 'Li': '锂', 'Be': '铍', 'Ne': '氖', 'Na': '钠', 'Mg': '镁', 'Al': '铝', 'Si': '硅', 'Cl': '氯',
                      'Ar': '氩', 'Ca': '钙', 'Sc': '钪', 'Ti': '钛', 'Cr': '铬', 'Mn': '锰', 'Fe': '铁', 'Co': '钴', 'Ni': '镍',
                      'Cu': '铜', 'Zn': '锌', 'Ga': '镓', 'Ge': '锗', 'As': '砷', 'Se': '硒', 'Br': '溴', 'Kr': '氪', 'Rb': '铷',
                      'Sr': '锶', 'Zr': '锆', 'Nb': '铌', 'Mo': '钼', 'Tc': '锝', 'Ru': '钌', 'Rh': '铑', 'Pd': '钯', 'Ag': '银',
                      'Cd': '镉', 'In': '铟', 'Sn': '锡', 'Sb': '锑', 'Te': '碲', 'Xe': '氙', 'Cs': '铯', 'Ba': '钡', 'Hf': '铪',
                      'Ta': '钽', 'Re': '铼', 'Os': '锇', 'Ir': '铱', 'Pt': '铂', 'Au': '金', 'Hg': '汞', 'Tl': '铊', 'Pb': '铅',
                      'Bi': '铋', 'Po': '钋', 'At': '砹', 'Rn': '氡', 'Fr': '钫', 'Ra': '镭', 'Rf': '𬬻', 'Db': '𬭊',
                      'Sg': '𬭳', 'Bh': '𬭛', 'Hs': '𬭶', 'Mt': '鿏', 'Ds': '𫟼', 'Rg': '𬬭', 'Nh': '鉨', 'Fl': '𫓧',
                      'Mc': '镆', 'La': '镧', 'Ce': '铈', 'Pr': '镨', 'Nd': '钕', 'Pm': '钷', 'Sm': '钐', 'Eu': '铕', 'Gd': '钆',
                      'Tb': '铽', 'Dy': '镝', 'Ho': '钬', 'Er': '铒', 'Tm': '铥', 'Yb': '镱', 'Lu': '镥', 'Ac': '锕', 'Th': '钍',
                      'Pa': '镤', 'Np': '镎', 'Pu': '钚', 'Am': '镅', 'Cm': '锔', 'Bk': '锫', 'Cf': '锎', 'Es': '锿', 'Fm': '镄',
                      'Md': '钔', 'No': '锘', 'Lr': '铹'
                      }

# 把限定条件更为严苛的同一特性的pattern放在相对宽松的pattern的下面
cha_pattern_list = [
    # re.compile(r'(抗拉强度).*?(\d{3,5}.*?\d{3,5}MPa)'),  # 抗拉强度控制在550～630MPa，抗拉强度≥1000MPa
    re.compile(r'(抗拉强度).*?(\d.*MPa)'),
    # re.compile(r'(屈服强度).*?(\d{3,5}.*?\d{3,5}MPa)'),  # 屈服强度95-145MPa，屈服强度≤700MPa
    re.compile(r'(屈服强度).*?(\d.*MPa)'),
    # re.compile(r'(.*率)(\d*.*?\d*%)'),  # 伸长率控制在23%-28%，延伸率(＞8%)
    re.compile(r'(.*率).*?(\d.*%)'),
    # re.compile(r'(.*比).*?(\d\.\d*.*?\d\.\d*)'),  # 屈强比为0.50～0.60
    re.compile(r'(.*比).*?(\d\.\d*.*)'),  # 屈强比为0.50, 屈强比为0.50～0.60
    re.compile(r'(断裂韧性).*?(\d.*)'),
    re.compile(r'(冲击韧性).*?(\d.*)'),  # 冲击韧性可达到40-85J/cm2, 冲击韧性23J/cm2
    re.compile(r'(.*?Akv).*?(\d.*)'),  # -60℃的Akv≥ 200J
    re.compile(r'(.*?冲击.*?功).*?(\d.*)'),  # -40℃下V型缺口冲击吸收功大于等于28.5J, -20℃冲击功(Akv)等于27J, 冲击功远大于40J
    re.compile(r'(焊接系数).*?(\d.*)'),  # 焊接系数达到0.9以上
    re.compile(r'(硬度).*?(\d.*)'),  # 硬度区间为280-340HB, 布氏硬度在370～430HB之间
    re.compile(r'(面缩指标).*?(\d.*)'),  # 面缩指标不低于35％
    re.compile(r'(厚度).*?(\d.*)')  # 厚度为20mm

]
# between_list = ['-', '~', '至', '～', '等于', '为']
over_list = ['以上', '大于', '大于等于', '达到', '提高至', '＞', '≥', '超过', '多于', '高于']
down_list = ['小于', '小于等于', '＜', '≤', '少于', '低于']

com_pattern_list = [
    re.compile(r'(\d.*?)的([碳氮氧氟硼磷硫钾钒钇碘钨铀氦锂铍氖钠镁铝硅氯氩钙钪钛铬锰铁钴镍铜锌镓锗砷硒溴氪铷锶锆铌钼锝钌铑钯银镉铟锡锑碲'
               r'氙铯钡铪钽铼锇铱铂金汞铊铅铋钋砹氡钫镭𬬻𬭊𬭳𬭛𬭶鿏𫟼𬬭鉨𫓧镆镧铈镨钕钷钐铕钆铽镝钬铒铥镱镥锕钍镤镎钚镅锔锫锎锿镄钔锘铹])'),
    re.compile(r'(\d.*?)的([奥马贝索]氏体)'),
    re.compile(r'(\d.*?)的(铁素体)'),
    re.compile(r'(\d.*?)的(珠光体)'),
    re.compile(r'([碳氮氧氟硼磷硫钾钒钇碘钨铀氦锂铍氖钠镁铝硅氯氩钙钪钛铬锰铁钴镍铜锌镓锗砷硒溴氪铷锶锆铌钼锝钌铑钯银镉铟锡锑碲'
               r'氙铯钡铪钽铼锇铱铂金汞铊铅铋钋砹氡钫镭𬬻𬭊𬭳𬭛𬭶鿏𫟼𬬭鉨𫓧镆镧铈镨钕钷钐铕钆铽镝钬铒铥镱镥锕钍镤镎钚镅锔锫锎锿镄钔锘铹]).*?(\d.*)'),
    re.compile(r'([碳氮氧氟硼磷硫钾钒钇碘钨铀氦锂铍氖钠镁铝硅氯氩钙钪钛铬锰铁钴镍铜锌镓锗砷硒溴氪铷锶锆铌钼锝钌铑钯银镉铟锡锑碲'
               r'氙铯钡铪钽铼锇铱铂金汞铊铅铋钋砹氡钫镭𬬻𬭊𬭳𬭛𬭶鿏𫟼𬬭鉨𫓧镆镧铈镨钕钷钐铕钆铽镝钬铒铥镱镥锕钍镤镎钚镅锔锫锎锿镄钔锘铹][+/或]\d*.*?'
               r'[碳氮氧氟硼磷硫钾钒钇碘钨铀氦锂铍氖钠镁铝硅氯氩钙钪钛铬锰铁钴镍铜锌镓锗砷硒溴氪铷锶锆铌钼锝钌铑钯银镉铟锡锑碲'
               r'氙铯钡铪钽铼锇铱铂金汞铊铅铋钋砹氡钫镭𬬻𬭊𬭳𬭛𬭶鿏𫟼𬬭鉨𫓧镆镧铈镨钕钷钐铕钆铽镝钬铒铥镱镥锕钍镤镎钚镅锔锫锎锿镄钔锘铹]).*?(\d.*)'),
    re.compile(r'([碳氮氧氟硼磷硫钾钒钇碘钨铀氦锂铍氖钠镁铝硅氯氩钙钪钛铬锰铁钴镍铜锌镓锗砷硒溴氪铷锶锆铌钼锝钌铑钯银镉铟锡锑碲'
               r'氙铯钡铪钽铼锇铱铂金汞铊铅铋钋砹氡钫镭𬬻𬭊𬭳𬭛𬭶鿏𫟼𬬭鉨𫓧镆镧铈镨钕钷钐铕钆铽镝钬铒铥镱镥锕钍镤镎钚镅锔锫锎锿镄钔锘铹]\+\d*.*?'
               r'[碳氮氧氟硼磷硫钾钒钇碘钨铀氦锂铍氖钠镁铝硅氯氩钙钪钛铬锰铁钴镍铜锌镓锗砷硒溴氪铷锶锆铌钼锝钌铑钯银镉铟锡锑碲'
               r'氙铯钡铪钽铼锇铱铂金汞铊铅铋钋砹氡钫镭𬬻𬭊𬭳𬭛𬭶鿏𫟼𬬭鉨𫓧镆镧铈镨钕钷钐铕钆铽镝钬铒铥镱镥锕钍镤镎钚镅锔锫锎锿镄钔锘铹]\+\d*.*?'
               r'[碳氮氧氟硼磷硫钾钒钇碘钨铀氦锂铍氖钠镁铝硅氯氩钙钪钛铬锰铁钴镍铜锌镓锗砷硒溴氪铷锶锆铌钼锝钌铑钯银镉铟锡锑碲'
               r'氙铯钡铪钽铼锇铱铂金汞铊铅铋钋砹氡钫镭𬬻𬭊𬭳𬭛𬭶鿏𫟼𬬭鉨𫓧镆镧铈镨钕钷钐铕钆铽镝钬铒铥镱镥锕钍镤镎钚镅锔锫锎锿镄钔锘铹]).*?(\d.*)'),
    re.compile(r'(铁素体组织).*?(大于\d.*)'),
    re.compile(r'(铁素体组织).*?(为\d.*)'),
    re.compile(r'([奥马贝索]氏体组织).*?(大于\d.*)'),
    re.compile(r'([奥马贝索]氏体组织).*?(为\d.*)'),
    re.compile(r'(珠光体组织).*?(大于\d.*)'),
    re.compile(r'(珠光体组织).*?(为\d.*)'),
]


def composition_key_value(com_list):
    com_list = preprocess(com_list)
    dict_list = []
    for com in com_list:
        com_dict = {}
        if '的' in com and re.search(com_pattern_list[0], com):
            temp_list = re.findall(com_pattern_list[0], com)[0]
            com_dict = {temp_list[1]: temp_list[0]}
        # elif re.search(pattern_list[1], com):
        #     temp_list = re.findall(pattern_list[1], com)[0]
        #     com_dict = {temp_list[0]: temp_list[1]}
        #     # print(com_dict)
        else:
            for index, com_pattern in enumerate(com_pattern_list):
                if index == 0:
                    continue
                elif index <= 3 and re.search(com_pattern, com):
                    temp_list = re.findall(com_pattern, com)[0]
                    relation_symbol = get_relation_symbol(com)
                    com_dict = {temp_list[1]: relation_symbol + temp_list[0]}
                elif index > 3 and re.search(com_pattern, com):
                    temp_list = re.findall(com_pattern, com)[0]
                    relation_symbol = get_relation_symbol(com)
                    com_dict = {temp_list[0]: relation_symbol + temp_list[1]}
        if com_dict:
            dict_list.append(com_dict)
    return dict_list


def characteristic_key_value(cha_list):
    dict_list = []
    for cha in cha_list:
        cha_dict = {}
        for cha_pattern in cha_pattern_list:
            if re.search(cha_pattern, cha):
                temp_list = re.findall(cha_pattern, cha)[0]
                # print(temp_list)
                relation_symbol = get_relation_symbol(cha)
                cha_dict = {temp_list[0]: relation_symbol + temp_list[1]}
        if cha_dict:
            dict_list.append(cha_dict)
    return dict_list


def get_relation_symbol(sen):
    relation_symbol = ''
    for over in over_list:
        if over in sen:
            relation_symbol = '≥'
    for down in down_list:
        if down in sen:
            relation_symbol = '≤'
    return relation_symbol


def preprocess(com_list):
    for index, com in enumerate(com_list):
        com = com.replace("：", "").replace("质量", "wt")
        for key, value in element_type_dict2.items():
            if key in com:
                com = com.replace(key, value)
                com_list[index] = com
        for key, value in element_type_dict1.items():
            if key in com:
                com_list[index] = com.replace(key, value)
    return com_list


if __name__ == "__main__":
    test_list_1 = ['C0.16％～0.20％', 'Si0.50％～0.70％', 'C：0.14%～0.17%', 'P≤0.015', 'C的量被限制为0.05%～0.11%',
                   'Si：0.15%～0.35%', '0.17％～0.20％的碳', 'C/Ti＞1.0%', 'Cu+C的质量大于1.5%', 'Mn+Cr+0.5Ni高于2.8％', '钒添加量超过0.20％',
                   'Mn+Cr+0.5Ni≤2.8％', 'Mn+Cr达到了3.94％', '5%～20%的奥氏体']
    print(composition_key_value(test_list_1))

    # pattern = re.compile(r'([碳氮氧氟硼磷硫钾钒钇碘钨铀氦锂铍氖钠镁铝硅氯氩钙钪钛铬锰铁钴镍铜锌镓锗砷硒溴氪铷锶锆铌钼锝钌铑钯银镉铟锡锑碲'
    #                      r'氙铯钡铪钽铼锇铱铂金汞铊铅铋钋砹氡钫镭𬬻𬭊𬭳𬭛𬭶鿏𫟼𬬭鉨𫓧镆镧铈镨钕钷钐铕钆铽镝钬铒铥镱镥锕钍镤镎钚镅锔锫锎锿镄钔锘铹][+/或]'
    #                      r'[碳氮氧氟硼磷硫钾钒钇碘钨铀氦锂铍氖钠镁铝硅氯氩钙钪钛铬锰铁钴镍铜锌镓锗砷硒溴氪铷锶锆铌钼锝钌铑钯银镉铟锡锑碲'
    #                      r'氙铯钡铪钽铼锇铱铂金汞铊铅铋钋砹氡钫镭𬬻𬭊𬭳𬭛𬭶鿏𫟼𬬭鉨𫓧镆镧铈镨钕钷钐铕钆铽镝钬铒铥镱镥锕钍镤镎钚镅锔锫锎锿镄钔锘铹]).*?(\d.*)')
    # temp = re.findall(pattern, '碳/钛＞1.0%')
    # print(temp)

    # pattern = re.compile(r'(.*比).*?(\d\.\d*.*)')  # 屈强比为0.50
    # temp = re.findall(pattern, '屈强比为0.50～0.60')
    # print(temp)

    test_list_2 = ['抗拉强度控制在550～630MPa', '抗拉强度≥1000MPa', '屈服强度95-145MPa', '屈服强度≤700MPa', '伸长率控制在23%-28%', '延伸率(＞8%)',
                   '屈强比为0.50～0.60', '屈强比为0.50', '冲击韧性可达到40-85J/cm2', '冲击韧性23J/cm2', '-60℃的Akv≥200J',
                   '-40℃下V型缺口冲击吸收功大于等于28.5J', '-20℃冲击功(Akv)等于27J', '冲击功远大于40J', '焊接系数达到0.9以上', '硬度区间为280-340HB',
                   '布氏硬度在370～430HB之间', '面缩指标不低于35％', '厚度为20mm']
    print(characteristic_key_value(test_list_2))

    # for value in element_type_dict2.values():
    #     print(value, end='')
