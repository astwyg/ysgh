import os
from webserver.settings import BASE_DIR


def find_keyword(keyword, path):
    path = os.path.join(BASE_DIR, path)
    msg = ""
    for root, dirs, files in os.walk(path):
        for f in files:
            with open(os.path.join(path, f),"r", encoding="utf-8") as fp:
                content = fp.read()
                keyword_times = content.count(keyword)
                if keyword_times:
                    msg += ("{}在{}中出现{}次".format(keyword,f,keyword_times)) + "\n"
    return msg


if __name__ == "__main__":
    print(BASE_DIR)
    keyword = input("输入关键字:")
    msg = find_keyword(keyword, path = "reportAna\\data\\annual_report_2018_txt")
    print(msg)