def webtext2data(text_path, data_path):
    with open(text_path, "r", encoding="utf-8") as f:
        webtext = f.read()
    webtext = webtext.replace("“", "").replace("”", "").replace("\"", "")
    x = open(data_path, "w", encoding="utf-8")
    for char in webtext:
        if char and char != "\n":
            if char == "。":
                x.write(char + " O\n\n")
            else:
                x.write(char + " O\n")


def data_division(origin_data_path, verification_data_path, train_data_path):
    with open(origin_data_path, "r") as origin_data_file:
        origin_data = origin_data_file.read()
    data_list = origin_data.split("\n\n")
    print(len(data_list))

    verify_count_write = 0
    train_count_write = 0

    with open(verification_data_path, "a") as verification_data_file:
        for index, data in enumerate(data_list):
            if index in [x * 10 + y for x in range(int(len(data_list) / 10)) for y in [1, 5, 9]]:
                verify_count_write += 1
                verification_data_file.write(data + "\n\n")

    with open(train_data_path, "a") as train_data_file:
        for index, data in enumerate(data_list):
            if index in [x * 10 + y for x in range(int(len(data_list) / 10)) for y in [0, 2, 3, 4, 6, 7, 8]]:
                train_count_write += 1
                train_data_file.write(data + "\n\n")
    print("验证集句子个数：", verify_count_write, "\n训练集句子个数：", train_count_write)


if __name__ == "__main__":
    webtext2data("./data/junshishiti5.txt", "./data/junshishiti5_data.txt")
    # data_division("./data/train_data.txt", "./data/example_dev.txt", "./data/example_train.txt")
