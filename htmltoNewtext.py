import html2text as ht
from zhihu import getWeb
import datetime
import os


def htmltotextmoudle(readDir, writeDir, today):
    text_maker = ht.HTML2Text()

    # 读取html格式文件
    fname = getWeb.fileIO(os.path.join("txt/newPage", datetime.datetime.strftime(today, '%Y-%m-%d'))+".txt", 0)

    for i in fname:
        name = (i.split("|"))[0] + ".html"

        if os.path.exists(os.path.join(writeDir, name[:-5]+".md")) or os.path.exists(os.path.join(writeDir[:-1], name[:-5]+".md")):
            print("已跳过%s！" % (name))
            pass
        else:
            with open(os.path.join(readDir, name), 'r', encoding='UTF-8') as f:
                htmlpage = f.read()
                f.flush()
                f.close()
            # 处理html格式文件中的内容
            text_temp1 = text_maker.handle(htmlpage)

            text_del_index_temp1 = -1
            text_del_index_temp2 = -1
            text_temp2 = list(text_temp1)
            for m in range(0, len(text_temp1)-2, 1):
                if text_del_index_temp1 == -1 and text_del_index_temp2 == -1:
                    if ord(text_temp2[m]) == 91:
                        text_del_index_temp1 = text_temp2.index(text_temp2[m])
                if text_del_index_temp1 != -1 and text_del_index_temp2 == -1:
                    if ord(text_temp2[m]) == 41:
                        text_del_index_temp2 = text_temp2.index(text_temp2[m])


            text_temp3 = (text_temp1[0:text_del_index_temp1]+text_temp1[text_del_index_temp2+16:-1])

            text = text_temp3.replace("https://www.zhihuban.ml", "http://zhihu.biada.cn:666")
            # text = text_temp1

            article = datetime.datetime.strftime(today, '%Y-%m-%d %H:%M:%S')

            sort_top = ""
            for l in name:
                if ord(l) > 57 or ord(l) < 48:
                    break
                else:
                    sort_top += l
            # 写入处理后的内容
            final_start = '---\n' + 'title: ' + name[:-5] + '\ndate: ' + article \
                          + '\ntags: ' + 'zhihu_new_vip' + '\ntop: ' + sort_top + "\n\n---\n"
            if len(text) >= 200:
                text_list = list(text)
                j = 60
                for k in range(60, len(text), 1):
                    if text_list[k] != "，":
                        j += 1
                    else:
                        text_list.insert(j, "<!--more-->")
                        break
                text = "".join(text_list)
            with open(os.path.join(writeDir, name[:-5]+".md"), 'w') as f:
                f.write(final_start + text + "\n[错误反馈](http://bbs.biada.cn:666/forum.php?mod=viewthread&tid=3&fromuid=1)")
                f.flush()
                f.close()

    print("已完成")


if __name__ == '__main__':
    today = datetime.datetime.now()
    htmltotextmoudle("NewWebPage1", "NewMdPage1", today)
