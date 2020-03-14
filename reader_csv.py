#coding = utf8
import csv
import json
import requests
import time
csv_file = 'csvdatetest.csv'
class request_csv:
    def __init__(self,csv_file):
        self.__csv_file=csv_file
    #读取csv数据并添加为列表
    def read_csv(self,filename):
        '''
        读取csv中的参数数据
        :param filename: testcsv文件路径
        日常使用可根据需要提取的参数对下面的字典进行更改即可
        '''
        try:
            print('开始读取数据...')
            with open(filename,'r',encoding='gbk') as fp:
                read = csv.DictReader(fp)
                read_dict = []
                for row in read:
                    ro = {}
                    ro['id'] = row['id']
                    ro['tid'] = row['tid']
                    ro['excpt'] = row['excpt']
                    ro['parames'] =row['parames']
                    read_dict.append(ro)
                return read_dict
        except FileNotFoundError:
            print('路径错误文件不存在')
            return read_dict

    #post 和 get 封装
    #get请求函数
    def __get_request(self,url,params=None):
        '''
        get 请求方法
        '''
        print('调运接口get...',url)
        with requests.get(url,params=params) as req:
            return req
    #post请求
    def __post_requests(self,url,data:dict):
        '''
        post 请求接口
        '''
        print('调用接口post...',url)
        with requests.post(url,data=json.dumps(data)) as req:
            return req

    #判断返回值
    def assert_verif_result(self,csv_result,assert_result):
        data = csv_result in str(assert_result)
        if data == True:
            return 'pass'
        else:
            return 'error'

    #对比两个dict参数的函数方法
    def assert_result(self,dict1:dict, dict2:dict, key_list):
        flag = True
        keys1 = dict1.keys()
        keys2 = dict2.keys()
        if len(key_list) != 0:
            for key in key_list:
                if key in keys1 and key in keys2:
                    if dict1[key] == dict2[key]:
                        flag = flag & True
                    else:
                        flag = flag & False
                else:
                    raise Exception('key_list contains error key')
        else:
            raise Exception('key_list is null')
        if flag:
            result = 'PASS'
        else:
            result = 'FAILED'
        return result


    def writecsv(self,filename, resultes):
        '''
        :param filename:放入csv文件
        :param resultes: 要存收入数据的列表
        :return:
        '''
        print('开始写入csv。。。。')
        with open(filename, 'w', encoding='gbk',newline="") as csvfile:
            header = 'id,tid,excpt,real_value,assert_value'.split(",")
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()  # 先写参数头部
            if resultes.__len__() > 0:
                for resulte in resultes:
                    writer.writerow(resulte)
            csvfile.close()
            print('写入结束')

    def run_mian(self):
        #指定最终结果生成的数据文件名称
        result_file = "result_{}.csv".format(str(time.time()).split('.')[0])

        #读取指定文件中的数据
        read_date = self.read_csv(self.__csv_file)

        if read_date.__len__() > 0: #检查read_date 中是否有数据有数据直接调用测试
            resulit = []
            for data in read_date:
                result = {}
                result['id'] = data['id']
                result['tid'] = data['tid']
                #组装参数
                params = {
                    "tid":data['tid'],
                    "interface":data['parames']
                }
                # 调用api测试
                real_value = self.__get_request(url="https://bbs.huaweicloud.com/forum/api/rest/index.php",params=params)
                # #调用assert方法判断
                result['excpt'] = data['excpt']
                assert_value = self.assert_verif_result(data['excpt'],assert_result=real_value.text)
                # print(assert_value)
                result['real_value'] = real_value.text
                result['assert_value'] = assert_value
                # 获取每一行里的字段以及实际结果和验证结果
                resulit.append(result)
            self.writecsv(result_file,resulit)
req = request_csv(csv_file)
req.run_mian()
