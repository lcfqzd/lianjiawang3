# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class Lianjiawang3Pipeline:
    fp = None

    # 重写父类的两个方法
    def open_spider(self, spider):
        print('我是open_spider(),我只会在爬虫开始的时候执行一次！')
        # self.fp = open('lianjia.txt', 'w', encoding='utf-8')
        # self.fp = open('nanan.txt', 'w', encoding='utf-8')
        self.fp = open('beibei.txt', 'w', encoding='utf-8')
        # self.fp = open('yubei.txt', 'w', encoding='utf-8')
        # self.fp = open('jiangbei.txt', 'w', encoding='utf-8')

    # 该方法是用来接收item对象。一次只能接收一个item，说明该方法会被调用多次
    # 参数item：就是接收到的item对象
    def process_item(self, item, spider):
        # print(item) #item其实就是一个字典
        # 将item存储到本文文件
        self.fp.write(item['title'] + ":" + item['addr'] + ":" + item['price'] + ":" + item['room'] + ":" +  item['direc'] + ":" + item['area'] + ":" + item['agent'] + '\n')

        return item  # 作用是将item返回给下一个即将提取的管道类使用，因为管道类是由优先级的，需要依次来

    def close_spider(self, spider):
        print('我是close_spider(),我只会在爬虫结束的时候执行一次！')
        self.fp.close()

# 存储到mysql数据库
class MysqlPipeLine(object):
    conn = None
    cursor = None

    def open_spider(self, spider):  # 连接对象只能被创建一次，open_spider()方法也只能一次，所以写在其中
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='spiders',charset='utf8')
        print(self.conn)

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()
        # sql = 'insert into lianjia values ("%s","%s","%s","%s","%s","%s","%s")' % (item['title'], item['addr'], item['price'], item['room'], item['direc'], item['area'], item['agent'])
        # sql = 'insert into nanan values ("%s","%s","%s","%s","%s","%s","%s")' % (item['title'], item['addr'], item['price'], item['room'], item['direc'], item['area'], item['agent'])
        # sql = 'insert into banan values ("%s","%s","%s","%s","%s","%s","%s")' % (item['title'], item['addr'], item['price'], item['room'], item['direc'], item['area'], item['agent'])
        # sql = 'insert into yubei values ("%s","%s","%s","%s","%s","%s","%s")' % (item['title'], item['addr'], item['price'], item['room'], item['direc'], item['area'], item['agent'])
        # sql = 'insert into jiangbei values ("%s","%s","%s","%s","%s","%s","%s")' % (item['title'], item['addr'], item['price'], item['room'], item['direc'], item['area'], item['agent'])
        sql = 'insert into beibei values ("%s","%s","%s","%s","%s","%s","%s")' % (item['title'], item['addr'], item['price'], item['room'], item['direc'], item['area'], item['agent'])

        # 事务处理
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

