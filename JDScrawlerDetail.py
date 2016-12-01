#-*-coding:utf-8-*-
#description: 京东详情页每日爬虫
#author：FSOL
#Python 3.5.2 64-bit
import json
import requests
import time
# 物品ID , 自营与否 , 商店ID , 运费 , 提示 , 有货状态 ,赠品 , 促销券,平均分，评论数，好评率，中评率，差评率，
def stock_put(x):
    if 'self_D' in x['stock'].keys():
        print('1 , '+str(x['stock']['self_D']['id'])+' , ',end='')
    else:
        print('0 , '+str(x['stock']['D']['id'])+' , ',end='')

    if x['stock']['dcashDesc']!='':
        print(x['stock']['dcashDesc'][:x['stock']['dcashDesc'].find('<a')]+' , ',end='')
    else:
        print(x['stock']['eir'][0]['iconSrc']+' , ',end='') 

    print('\"'+x['stock']['Ext']+'\"'+' , ',end='') 

    print(str(x['stock']['StockState'])+' , ',end='')
#赠品 , 促销券, 其它,
def cuxiao_put(x):
    if x['prom']['tags'] != []:
        print('\"',end='')
        for i in x['prom']['tags'][0]['gifts']:
            print(i['nm']+' , ',end='')
        print('\" , ',end='')
    if x['skuCoupon'] !=[]:
        print('\"',end='')
        for i in x['skuCoupon']:
            print('满'+str(i['quota'])+'减'+str(i['discount'])+' , ',end='')
        print('\" , ',end='')
    if x['pickOneTag']!=[]:
        print('\"',end='')
        for i in x['pickOneTag']:
            print(i['content']+' , ',end='')
        print('\" , ',end='')
#平均分，评论数，好评率，中评率，差评率，
def comment_put(x):
    x = x['CommentsCount'][0]
    print(str(x['AverageScore'])+' , '+str(x['CommentCount'])+' , '+str(x['GoodRate'])+' , '\
                                      +str(x['GeneralRate'])+' , '+str(x['PoorRate'])+' , ',end='')
def main(itemid):
    time.sleep(0.5)
    print(str(itemid)+' , ',end='')
    url = 'https://c0.3.cn/stock?skuId='+str(itemid)+'&venderId=1000040122&cat=1320,1584,2675&area=1_72_2799_0&buyNum=1&extraParam={%22originid%22:%221%22}&ch=1&pduid=655718568&pdpin='
    req = requests.get(url)
    stock = json.loads(req.content.decode('gbk'))
    url = 'https://cd.jd.com/promotion/v2?skuId='+str(itemid)+'&area=17_1441_41909_0&shopId=57617&venderId=61908&cat=652%2C654%2C832&_=1480602489906'
    req = requests.get(url)
    cuxiao = json.loads(req.content.decode('gbk'))
    url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds='+str(itemid)+'&_=1480603977503'
    req = requests.get(url)
    comment = json.loads(req.content.decode('gbk'))
    stock_put(stock)
    cuxiao_put(cuxiao)
    comment_put(comment)
