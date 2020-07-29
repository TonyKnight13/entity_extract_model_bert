def verify():
    path = "./data/hejin/hejin_train_data.txt"
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    s_list = s.split("\n\n")
    s_list = [s for s in s_list if s != ""]
    with open(path, "w", encoding="utf-8") as f:
        for s in s_list:
            f.write(s + "\n\n")
    chunk_tags = ['O', 'B-CAT', 'I-CAT', 'B-FEA', 'I-FEA', "B-COM", "I-COM", "B-CRA", "I-CRA"]
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    word_list = s.split("\n")
    for index, word in enumerate(word_list):
        count = 0
        if word != "":
            char_list = word.split(" ")
            if len(char_list) < 1:
                print(index)
            # print(char_list)
            for tag in chunk_tags:
                try:
                    if tag == char_list[1]:
                        count = 1
                except:
                    print(index)
            if count == 0:
                print(index + 1, "Tag Error!")
            if word_list[index + 1] != "":
                temp_list = word_list[index + 1].split(" ")
                try:
                    if char_list[1][0] == "O" and temp_list[1][0] == "I":
                        print(index, "I Error!")
                    if char_list[1][0] == "B" and temp_list[1][0] == "B":
                        print(index, "B Error!")
                    if char_list[1][0] == "B" and temp_list[1][0] == "O":
                        print(index, "B Error!")
                    if char_list[1][0] == "I" and temp_list[1][0] == "I" and char_list[1] != temp_list[1]:
                        print(index, "I Error!")
                    if char_list[1][0] == "B" and temp_list[1][0] == "I" and char_list[1][1:] != temp_list[1][1:]:
                        print(index, "B Error!")
                except:
                    print(index)

if __name__ == '__main__':
    verify()