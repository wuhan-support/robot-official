import json
import pandas as pd
# from upload_latest_json import main

def get_latest_data(filename="latest.json"):
    """ 
    用来获取最近一次的数据，通过解析jsons/latest.json文件
    返回值为DataFrame，需要进入transfer_pro_to_ct或者sv_account.py里的pushData进行二次处理
    """
    f = open("jsons/%s"%filename,'r',encoding='utf-8')
    for line in f:
        dic=json.loads(line)
        Area = dic[ 'data' ]['listByArea']
        city=[]
        for i in Area:
            for j in i['cities']:
                cites_dict = {}
                cites_dict[ 'provinceName' ] = i[ 'provinceName' ]
                
                cites_dict[ 'provinceAbbreviation' ] = i[ 'provinceShortName' ]
                cites_dict[ 'city']= j['cityName']
                cites_dict[ 'confirmed']=j['confirmed']
                cites_dict[ 'suspected']=j['suspected']
                cites_dict[ 'cured']=j['cured']
                cites_dict[ 'dead']=j['dead']
                #解决重名
                if cites_dict['provinceAbbreviation']=="辽宁" and cites_dict['city']=="朝阳":
                    cites_dict['city']='辽宁朝阳'
                city.append(cites_dict)

        return pd.DataFrame(city)

def transfer_pro_to_ct(df):
    """
    上海 	外地来沪人员 浦东新区 长宁区 静安区 徐汇区 虹口区 闵行区 青浦区 黄浦区 宝山区 嘉定...
    将省市与城市对应
    """
    def func(x):
        result = ""
        for i in x:
            result+=i+" "
        return result
    return df[["provinceAbbreviation","city"]].groupby("provinceAbbreviation").agg(func)

def get_all_city(df):
    """
    获得所有城市
    """
    return list(df["city"].values)

# if __name__=="main":
    # main()
    # get_latest_data()