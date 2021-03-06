import requests
import pymysql, time, threading
import contextlib


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql_local(host='localhost', port=3333, user='root', password='kuaikang', db='kuaik', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    conn.autocommit(True)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


def get_question_ids(cur, subject_key, chapter_id):
    sql = "SELECT question_id from {subject_key}_chapter_question WHERE chapter_id = '{chapter_id}'"
    cur.execute(sql.format(subject_key=subject_key, chapter_id=chapter_id))
    return cur.fetchall()


def get_question(cur, subject_key, question_id):
    sql = "SELECT context,question_type,difficult,answer_url from {subject_key}_question WHERE question_id = '{question_id}' and answer_url is not null"
    cur.execute(sql.format(subject_key=subject_key, question_id=question_id))
    return cur.fetchall()


def get_tag(cur, subject_key, question_id):
    sql = "SELECT tag_url from {subject_key}_tag_question WHERE question_id = '{question_id}'"
    cur.execute(sql.format(subject_key=subject_key, question_id=question_id))
    return cur.fetchone()


def get_item(cur, subject_key, question_id):
    sql = "SELECT context,`option` from {subject_key}_item WHERE question_id = '{question_id}'"
    cur.execute(sql.format(subject_key=subject_key, question_id=question_id))
    return cur.fetchall()


def main(currentSubject, importChapterName, import_Chapter, zujuan_chapter):
    print(importChapterName)
    head = {
        "Content-Type": "application/json"
    }
    with mysql_local() as cur:
        question_ids = get_question_ids(cur, currentSubject, zujuan_chapter)
        for question_id in question_ids:
            question = get_question(cur, currentSubject, question_id.get('question_id'))
            for q in question:  # context,type,difficult,answer_url
                req = {"currentSubject": currentSubject, "questionContent": q.get('context'),
                       "importChapterId": import_Chapter,
                       "questionType": "11"}
                tag = get_tag(cur, currentSubject, question_id.get('question_id'))
                if tag:
                    req["tagUrl"] = tag.get('tag_url')
                else:
                    req["tagUrl"] = ""
                req["importChapterName"] = importChapterName
                req["answerUrl"] = q.get('answer_url')
                req["difficult"] = q.get('difficult')
                items = get_item(cur, currentSubject, question_id.get('question_id'))
                item = []
                for it in items:  # context,`option`
                    item.append({"content": it.get('context'), "option": it.get('option')})
                req["items"] = item
                resp = requests.post(url="http://localhost:28870/exue-question-system/spark/save", headers=head,
                                     json=req)


def trans(subject, data):
    for d in data:
        main(subject, d[0], d[1], d[2])


if __name__ == '__main__':
    li = [['一、准备课', '020001001004034001001', '106788'], ['二、位置', '020001001004034001002', '106792'],
          ['三、1~5的认识和加减法', '020001001004034001003', '3821'], ['四、认识图形（一）', '020001001004034001004', '3822'],
          ['五、6~10的认识和加减法', '020001001004034001005', '3824'], ['六、11~20各数的认识', '020001001004034001006', '3825'],
          ['七、认识钟表', '020001001004034001007', '3826'], ['八、20以内的进位加法', '020001001004034001008', '11644'],
          ['一、认识图形（二）', '020001002004034001001', '96832'], ['二、20以内的退位减法', '020001002004034001002', '106736'],
          ['三、分类与整理', '020001002004034001003', '96834'], ['四、100以内数的认识', '020001002004034001004', '106737'],
          ['五、认识人民币', '020001002004034001005', '106738'], ['六、100以内的加法和减法（一）', '020001002004034001006', '106739'],
          ['七、找规律', '020001002004034001007', '96838'], ['一、长度单位', '020002001004034001001', '106803'],
          ['二、100以内的加法和减法（二）', '020002001004034001002', '3839'], ['三、角的初步认识', '020002001004034001003', '84370'],
          ['四、表内乘法（一）', '020002001004034001004', '3841'], ['五、观察物体（一）', '020002001004034001005', '106818'],
          ['六、表内乘法（二）', '020002001004034001006', '3843'], ['七、认识时间', '020002001004034001007', '106804'],
          ['八、数学广角、搭配（一）', '020002001004034001008', '106820'], ['一、数据收集整理', '020002002004034001001', '96820'],
          ['二、表内除法（一）', '020002002004034001002', '106714'], ['三、图形的运动（一）', '020002002004034001003', '96822'],
          ['四、表内除法（二）', '020002002004034001004', '106715'], ['五、混合运算', '020002002004034001005', '106716'],
          ['六、有余数的除法', '020002002004034001006', '96825'], ['七、万以内数的认识', '020002002004034001007', '106713'],
          ['八、克和千克', '020002002004034001008', '96828'], ['九、数学广角──推理', '020002002004034001009', '96829'],
          ['一、时、分、秒', '020003001004034001001', '106834'], ['二、万以内的加法和减法（一）', '020003001004034001002', '106827'],
          ['三、测量', '020003001004034001003', '3857'], ['四、万以内的加法和减法（二）', '020003001004034001004', '3858'],
          ['五、倍的认识', '020003001004034001005', '106828'], ['六、多位数乘一位数', '020003001004034001006', '3862'],
          ['七、长方形和正方形', '020003001004034001007', '106830'], ['八、分数的初步认识', '020003001004034001008', '106842'],
          ['九、数学广角—集合', '020003001004034001009', '106831'], ['一、位置与方向（一）', '020003002004034001001', '3867'],
          ['二、除数是一位数的除法', '020003002004034001002', '3868'], ['三、复式统计表', '020003002004034001003', '3869'],
          ['四、两位数乘两位数', '020003002004034001004', '3870'], ['五、面积', '020003002004034001005', '3871'],
          ['七 小数的初步认识', '020003002004034001008', '3872'], ['八、数学广角——搭配（二）', '020003002004034001009', '106760'],
          ['一、大数的认识', '020004001004034001001', '3876'], ['二、公顷和平方千米', '020004001004034001002', '98995'],
          ['三、角的度量', '020004001004034001003', '3877'], ['四、三位数乘两位数', '020004001004034001004', '3878'],
          ['五、平行四边形和梯形', '020004001004034001005', '3879'], ['六、除数是两位数的除法', '020004001004034001006', '3880'],
          ['七、条形统计图', '020004001004034001007', '104332'], ['八、数学广角—优化', '020004001004034001008', '3882'],
          ['1亿有多大', '020004001004034001012', '84560'], ['一、四则运算', '020004002004034001001', '3884'],
          ['二、观察物体（二）', '020004002004034001002', '104333'], ['三、运算定律', '020004002004034001003', '3886'],
          ['四、小数的意义和性质', '020004002004034001004', '3887'], ['五、三角形', '020004002004034001005', '3888'],
          ['六、小数的加法和减法', '020004002004034001006', '3889'], ['七、图形的运动（二）', '020004002004034001007', '104334'],
          ['八、平均数与条形统计图', '020004002004034001008', '104335'], ['九、数学广角——鸡兔同笼', '020004002004034001010', '3891'],
          ['一、小数乘法', '020005001004034001001', '3893'], ['二、位置', '020005001004034001002', '98998'],
          ['三、小数除法', '020005001004034001003', '3894'], ['四、可能性', '020005001004034001004', '98999'],
          ['五、简易方程', '020005001004034001005', '3896'], ['六、多边形的面积', '020005001004034001006', '3897'],
          ['七、数学广角—植树问题', '020005001004034001007', '3899'], ['八、总复习', '020005001004034001008', '106860'],
          ['掷一掷', '020005001004034001011', '106859'], ['一、观察物体（三）', '020005002004034001001', '104365'],
          ['二、因数与倍数', '020005002004034001002', '3902'], ['三、长方体和正方体', '020005002004034001003', '3903'],
          ['四、分数的意义和性质', '020005002004034001005', '3904'], ['五、图形的运动（三）', '020005002004034001006', '104367'],
          ['六、分数的加法和减法', '020005002004034001007', '3905'], ['七、折线统计图', '020005002004034001009', '106267'],
          ['一、分数乘法', '020006001004034001001', '3910'], ['二、位置与方向（二）', '020006001004034001002', '3909'],
          ['三、分数除法', '020006001004034001003', '3911'], ['四、比', '020006001004034001004', '104288'],
          ['五、圆', '020006001004034001005', '3912'], ['六、百分数（一）', '020006001004034001006', '3913'],
          ['七、扇形统计图', '020006001004034001007', '3914'], ['八、数学广角—数与形', '020006001004034001008', '3915'],
          ['确定起跑线', '020006001004034001012', '104289'], ['节约用水', '020006001004034001013', '104290'],
          ['一、负数', '020006002004034001001', '3917'], ['二、百分数（二）', '020006002004034001002', '104301'],
          ['三、圆柱与圆锥', '020006002004034001004', '47499'], ['四、比例', '020006002004034001005', '3922'],
          ['五、数学广角——鸽巢问题', '020006002004034001007', '3925']]
for i in range(4):
    count = 25
    t = threading.Thread(target=trans, args=("sx", li[count * i:count * i + count],))
    t.start()
