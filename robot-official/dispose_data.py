import json
import pandas as pd
# from upload_latest_json import main
from constant import ALL_CHINA
class Data:
    """
    把数据处理成推送的形式
    """
    def __init__(self,r):
        self.r=r
        self.data=self.get_latest_data()#DataFrame
        self.province_to_cities=(self.transfer_pro_to_ct(self.data))['city']#Series province->city(string，空格隔开)
        self.all_city=self.get_all_city(self.data)#list
        self.cities_to_province=self.transfer_ct_to_pro(self.data)#Series
        self.series=self.pushData()#Series
        self.all_pros=self.get_all_pro(self.data)#list
    def get_latest_data(self,filename="latest.json"):
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

    def transfer_pro_to_ct(self,df):
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

    def get_all_city(self,df):
        """
        获得所有城市
        """
        return list(df["city"].values)

    def pushData(self):
        """
        对确诊，治愈和死亡人数进行字符串拼接，并以城市为index，拼接的字符串作为value存储
        在series中并返回
        """
        df=self.get_latest_data()
        df=df.applymap(lambda x: str(x))
        df=df.set_index("city")
        series = "确诊:" + df["confirmed"] + " 治愈:" + df["cured"] + " 死亡:" + df["dead"]
        return series

    def updateData(self, new_data):
        """
        判断数据是否更新，获得更新的series，并返回
        """
        old_series=self.series
        new_series=new_data.series
        # print("*" * 10)
        # print(new_series)
        # print("*" * 10)
        # print(old_series)
        update_list=[]
        old_cities=old_series.index
        new_cities=new_series.index
        diff_cities=list(set(new_cities)-set(old_cities))
        # print("ln"*10)
        # print(old_series)
        flag_list=(old_series!=new_series[old_cities]).values
        # print("1"*10)
        # print(flag_list)
        if len(diff_cities)>0:
            # self.push_diff_cities_to_db(diff_cities)
            update_list.extend(diff_cities)
        update_cities=(old_series[flag_list]).index
        # print("ln1"*10)
        if len(update_cities)>0:
            update_list.extend(update_cities)
        # print("eo"*10)
        print(update_cities)
        city_to_uid=self.push_cty_pro_to_update(update_cities)
        if len(update_cities)>0:
            
            return new_series[update_cities],city_to_uid
        else:
            return pd.Series(),city_to_uid
    def push_diff_cities_to_db(self,diff_cities):
        """
        将新增加的城市加入数据库中
        """
         
        return ""
    def push_cty_pro_to_update(self,update_cities):
        all_keys=self.r.get_all_keys()
        city_to_uid={}
        for update_city in update_cities:
            pro=self.cities_to_province[update_city]
            city_to_uid[update_city]=list()
            if pro in all_keys:
                pro_uid=self.r.get_subscribed_users(pro)
                city_to_uid[update_city].extend(pro_uid)
            if update_city in all_keys:
                city_to_uid[update_city].extend(self.r.get_subscribed_users(update_city))
            if ALL_CHINA in all_keys:
                city_to_uid[update_city].extend(self.r.get_subscribed_users(ALL_CHINA))
            city_to_uid[update_city]=set(city_to_uid[update_city])
        return city_to_uid
    def transfer_ct_to_pro(self,df):
        """
        通过城市查询所在省份
        """      
        df=df.set_index("city")
        series=df["provinceAbbreviation"]
        return series
    def get_all_pro(self,df):
        """
        拿到所有省份数据
        """
        return list(set(df["provinceAbbreviation"].values))

# if __name__=="main":
    # main()
    # get_latest_data()