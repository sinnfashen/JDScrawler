#-*-coding:utf-8-*-
#description: 京东详情页每日爬虫
#author：FSOL
#Python 2.7.12 64-bit
import json
import requests
import time
fout = open('output.csv','a',encoding='UTF-8')
def put(x,stop=True):
    if stop:
        fout.write('{}{}'.format(x,' , '))
    else:
        fout.write(x)
# 有货状态 , 运费 , 提示 ,
def stock_put(itemid):
    url = 'https://c0.3.cn/stock?skuId={}&cat=670,12800,12801&area=17_1441_41909_0&extraParam={%22originid%22:%221%22}'.format(itemid)
    req = requests.get(url)
    x = json.loads(req.content.decode('gbk'))

    put(x['stock']['StockState'])
    if(x['stock']['StockState']!=34):
        if x['stock']['dcashDesc']!='':
            put(x['stock']['dcashDesc'][:x['stock']['dcashDesc'].find('<a')])
        else:
            put(x['stock']['eir'][0]['iconSrc'])
    else:
        put('')

    put('\" {} \"'.format(x['stock']['Ext']))
    
# 自营与否 , 商店ID , 
def vender_put(itemid):
    url ='https://c0.3.cn/stocks?type=batchstocks&skuIds={}&area=17_1441_41909_0'.format(itemid)
    req = requests.get(url)
    x = json.loads(req.content.decode('gbk'))
    
    if 'self_D' in x[str(itemid)].keys():
        put(1),put(x[str(itemid)]['self_D']['id'])
    else:
        put(0),put(x[str(itemid)]['D']['id'])
#赠品 , 促销券, 其它促销手段,
def cuxiao_put(itemid):

    url = 'https://cd.jd.com/promotion/v2?skuId={}&area=17_1441_41909_0&shopId=57617&venderId=61908&cat=652%2C654%2C832&_=1480602489906'.format(itemid)
    req = requests.get(url)
    x = json.loads(req.content.decode('gbk'))
    
    if x['prom']['tags'] != []:
        put('\"',False)
        for i in x['prom']['tags'][0]['gifts']:
            put(i['nm'])
        put('\"',False)
    put('')
    if x['skuCoupon'] !=[]:
        put('\"',False)
        for i in x['skuCoupon']:
            put('满{}减{}'.format(i['quota'], i['discount']))
        put('\"',False)
    put('')
    if x['prom']['pickOneTag']!=[]:
        put('\"',False)
        for i in x['pickOneTag']:
            put(i['content'])
        put('\"',False)
    put('')
#平均分，评论数，好评率，中评率，差评率，
def comment_put(itemid):

    url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}'.format(itemid)
    req = requests.get(url)
    x = json.loads(req.content.decode('gbk'))
    
    x = x['CommentsCount'][0]
    put(x['AverageScore']),put(x['CommentCount']),put(x['GoodRate']),put(x['GeneralRate']),put(x['PoorRate'])
#价格
def price_put(itemid):

    url = 'https://p.3.cn/prices/get?skuid=J_{}'.format(itemid)
    req = requests.get(url)
    x = json.loads(req.content.decode('gbk')[1:-2])

    put(x['p'])

def work(itemid):
    try:
        price_put(itemid)
        comment_put(itemid)
        cuxiao_put(itemid)
        vender_put(itemid)
        stock_put(itemid)
    except Exception as e:
        return -1
    else:
        return 0
