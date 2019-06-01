import requests
from lxml import etree
import pymysql
import re

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
          'Referer': 'https://img.t.sinajs.cn/t4/appstyle/searchpc/css/pc/css/global.css?version=20190515175300',
          }
#网址，需要改12：3   3需要改
url = 'https://s.weibo.com/user?q=&auth=per_vip&region=custom:12:3&page='
#页数，也是要改的
for i in range(1,51):
    url_n = url + str(i)
    response = requests.get(url_n,headers=header).text
    html = etree.HTML(response)
    #开始提取一页所有文字
    shuoyou = html.xpath('//*[@id="pl_user_feedList"]/div')
    for suoyou in shuoyou:
        # 名字
        name = suoyou.xpath('./div[2]/div/a/text()')[0]         #名字
        #url
        urlss = suoyou.xpath('./div[2]/div/a/@href')[0]
        #写入数据库的格式
        urls = 'http:' + urlss
        sex = ''
        adds= ''
        shenfen = ''
        funs = ''
        jianjie = ''
        jiaoyu = ''
        biaoqian = ''
        zhiye=''
        cccc = shuoyou.index(suoyou)
        zzzz = '//*[@id="pl_user_feedList"]/div[@class="card card-user-b s-pg16 s-brt1"][%s]/div[@class="info"]/p' %(cccc + 1)
        pp = suoyou.xpath(zzzz)
        for l in range(len(pp)):
            #性别
            if l == 0:
                #global sex
                sexs = pp[0].xpath('./i/@class')[0]
                if sexs == 'icon-sex icon-sex-female':
                    sex = 'girl'
                elif sexs == 'icon-sex icon-sex-male':
                    sex = 'boy'
                # 地址
                #global adds
                addss = pp[0].xpath('./text()')[1]
                p = re.compile(r'[\u4e00-\u9fa5]')
                ccc = re.findall(p, addss)
                zz = ''.join(ccc)
                adds = zz
                # 身份
            if l == 1:
                #global shenfen
                shenfens = pp[1].xpath('./text()')
                if shenfens == []:
                    shenfen = ''
                else:
                    shenfen = shenfens[0]
            # 粉丝数量
            if l == 2:
                #global funs
                funss = pp[2].xpath('./span[2]/a/text()')
                if funss == []:
                    funs = ''
                else:
                    funs = funss[0]
            if l >= 3:
                aaa = pp[l].xpath('.//text()')
                #aaaa = ''.join(aaa)
                aaaa = " ".join('%s' % id for id in aaa)
                if '简介' in aaaa:
                    #global jianjie
                    jianjie = aaaa
                elif '标签' in aaaa:
                    #global biaoqian
                    biaoqian = aaaa
                elif '教育信息' in aaaa:
                    #global jiaoyu
                    jiaoyu = aaaa
                elif '职业信息' in aaaa:
                    #global zhiye
                    zhiye = aaaa
        #写入数据库
        db = pymysql.connect(host='localhost',user='root',password='amiao0908',port=3306,db='amiao')
        cursor = db.cursor()
        #写入表名
        sql = 'INSERT INTO weibo_copy3(name,url,adds,sex,funs,shenfen,biaoqian,jianjie,jiaoyu,zhiye) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql,(name,urls,adds,sex,funs,shenfen,biaoqian,jianjie,jiaoyu,zhiye))
            db.commit()
        #数据回滚，防止写断
        except:
            db.rollback()
            db.close()