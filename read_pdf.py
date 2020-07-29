import pdfplumber

for i in range(1, 51):
    zhuanli_path = data + str(i) +".pdf"
    with pdfplumber.open(zhuanli_path) as pdf:
        page_count = len(pdf.pages)
        # print(page_count)
        text_list = []
        text_all = ''
        for page in pdf.pages:
            # print('---------- 第[%d]页 ----------' % page.page_number)
            text_list.append(page.extract_text())
            # text_all += page.extract_text()
        # print(text_list)
