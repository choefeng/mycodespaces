import html2text as ht
from zhihu import getWeb
import datetime
import os


def htmltotextmoudle(readDir, writeDir, today):
    text_maker = ht.HTML2Text()

    # 读取html格式文件
    fname = getWeb.fileIO(os.path.join("txt", datetime.datetime.strftime(today, '%Y-%m-%d'))+".txt", 0)
    for i in fname:
        name = ""
        if i[7:8] == "A":
            name = i[14:]
        elif i[7:8] == "B":
            name = i[12:]

        if os.path.exists(os.path.join(writeDir, name)) or os.path.exists(os.path.join(writeDir[:-1], name)):
            print("已跳过%s！" % (name))
            pass
        else:
            with open(os.path.join(readDir, name), 'r', encoding='UTF-8') as f:
                htmlpage = f.read()
                f.flush()
                f.close()
            # 处理html格式文件中的内容
            text = text_maker.handle(htmlpage)

            article = datetime.datetime.strftime(today, '%Y-%m-%d %H:%M:%S')

            sort_top = ""
            for l in name:
                if ord(l) > 57 or ord(l) < 48:
                    break
                else:
                    sort_top += l
            # 写入处理后的内容
            final_start = '---\n' + 'title: ' + name[:-3] + '\ndate: ' + article \
                          + '\ntags: ' + 'zhihu_vip' + '\ntop: ' + sort_top + "\n\n---\n"
            if len(text) >= 100:
                text_list = list(text)
                j = 90
                for k in range(90, len(text), 1):
                    if text_list[k] != "，":
                        j += 1
                    else:
                        text_list.insert(j, "<!--more-->")
                        break
                text = "".join(text_list)
            with open(os.path.join(writeDir, name), 'w') as f:
                f.write(final_start + text)
                f.flush()
                f.close()

    print("已完成")


if __name__ == '__main__':
    today = datetime.datetime.now()
    htmltotextmoudle("webPage1", "mdPage1", today)
