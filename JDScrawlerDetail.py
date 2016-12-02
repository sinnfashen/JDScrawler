#-*-coding:utf-8-*-
#description: 京东详情页每日爬虫
#author：FSOL
#Python 3.5.2 64-bit
import json
import requests
import time
# 自营与否 , 商店ID , 运费 , 提示 , 有货状态 ,
def put(x):
    print(str(x)+' , ',end='')
# 有货状态 , 运费 , 提示 ,
def stock_put(itemid):
    url = 'https://c0.3.cn/stock?skuId=' + str(itemid)+'&cat=670,12800,12801&area=17_1441_41909_0&extraParam={%22originid%22:%221%22}'
    req = requests.get(url)
    x = json.loads(req.content.decode('gbk'))

    put(str(x['stock']['StockState']))
    if(x['stock']['StockState']!=34):
        if x['stock']['dcashDesc']!='':
            put(x['stock']['dcashDesc'][:x['stock']['dcashDesc'].find('<a')])
        else:
            put(x['stock']['eir'][0]['iconSrc'])
    else:
        put('')

    put('\"'+x['stock']['Ext']+'\"') 
    
# 自营与否 , 商店ID , 
def vender_put(itemid):
    url ='https://c0.3.cn/stocks?type=batchstocks&skuIds='+str(itemid)+'&area=17_1441_41909_0'
    req = requests.get(url)
    x = json.loads(req.content.decode('gbk'))
    
    if 'self_D' in x[str(itemid)].keys():
        put(1),put(x[str(itemid)]['self_D']['id'])
    else:
        put(0),put(x[str(itemid)]['D']['id'])
#赠品 , 促销券, 其它促销手段,
def cuxiao_put(itemid):

    url = 'https://cd.jd.com/promotion/v2?skuId='+str(itemid)+'&area=17_1441_41909_0&shopId=57617&venderId=61908&cat=652%2C654%2C832&_=1480602489906'
    req = requests.get(url)
    x = json.loads(req.content.decode('gbk'))
    
    if x['prom']['tags'] != []:
        print('\"',end='')
        for i in x['prom']['tags'][0]['gifts']:
            put(i['nm'])
        print('\"',end='')
    put('')
    if x['skuCoupon'] !=[]:
        print('\"',end='')
        for i in x['skuCoupon']:
            put('满'+str(i['quota'])+'减'+str(i['discount']))
        print('\"',end='')
    put('')
    if x['prom']['pickOneTag']!=[]:
        print('\"',end='')
        for i in x['pickOneTag']:
            put(i['content'])
        print('\"',end='')
    put('')
#平均分，评论数，好评率，中评率，差评率，
def comment_put(itemid):

    url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds='+str(itemid)
    req = requests.get(url)
    x = json.loads(req.content.decode('gbk'))
    
    x = x['CommentsCount'][0]
    put(x['AverageScore']),put(x['CommentCount']),put(x['GoodRate']),put(x['GeneralRate']),put(x['PoorRate'])
#价格
def price_put(itemid):

    url = 'https://p.3.cn/prices/get?skuid=J_'+str(itemid)
    req = requests.get(url)
    x = json.loads(req.content.decode('gbk')[1:-2])

    put(x['p'])

if __name__ == '__main__':
    itemid=input()
    price_put(itemid)
    comment_put(itemid)
    cuxiao_put(itemid)
    vender_put(itemid)
    stock_put(itemid)
