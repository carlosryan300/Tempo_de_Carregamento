from google.cloud import bigquery
from oauth2client.service_account import ServiceAccountCredentials as sac
from pandas import DataFrame
import gspread, socket
from time import sleep
from requests import api



class Time_load():
    def __init__(self):
        self.client = bigquery.Client(project='project_Id')
        self.dataset = self.client.dataset(dataset_id='whp_time_loading').table('home_institucional_loja_concorrentes')
        self.table = self.client.get_table(self.dataset)
        self.connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.escopo = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        self.credencial = sac.from_json_keyfile_name('./json/credential.json', self.escopo)
        self.authorize = gspread.authorize(self.credencial) 
        self.sheet = Time_load.sheets(self)
        self.urls = list()
    def insert(self, tuple_insert):
        insert_rows = self.client.insert_rows(table=self.table, rows=tuple_insert)
        print(insert_rows)
    def conection(self):
        self.connect.settimeout(2)
        connect = self.connect.connect_ex(('www.google.com', 80))
        if connect == 0:
            return True
        else:
            while connect != 0:
                sleep(30)
                connect = self.connect.connect_ex(('www.google.com', 80))
            return True

        keys = list(filter(None,
                            list(
                            DataFrame(self.authorize
                           .open_by_key('10LLdOcHvSsTbzdbkoWL9KyZhl9Yum24fuhQjB8alzDg')
                           .worksheet('API')
                           .get_all_records())['API_KEY'])))
        Types = ["3GSlow", "Cable", "4G"]
        return [sites, keys, Types]

    def mount_url(self, url, tipo):
        mount = f"http://www.webpagetest.org/runtest.php?k={self.sheet[1][0]}&url={url}&breakdown=1&runs=1&fvonly=0&f=json&location=SaoPaulo_BR:Chrome.{tipo}"
        return mount
    def request(self, url):
        return_req = api.get(url=url).json()
        if 200 >= return_req['statusCode'] and 299 <= return_req['statusCode']:
            return return_req
        else:
            return 'erro'
    def webpage_test(self):
        tl = Time_load()
        for ty in self.sheet[2]:
            for ur in self.sheet[0]:
                req = tl.request(tl.mount_url(ur, ty))
                if req == 'erro':
                    self.sheet.remove(self.sheet[1][0])
                    req = tl.request(tl.mount_url(ur, ty))
                self.urls.append(req['data']['jsonUrl'])
        return self.urls
    def webpage_wait(self):
        tl = Time_load()
        tl.webpage_test()
        sleep(len(self.urls)*45)
        url = self.urls[len(self.urls)-1]
        req = tl.request(url)
        if req == 'erro':
            while True:
                sleep(180)
                req = tl.request(url)
                if req != 'erro':
                    break
        return True
    def webpage_result(self):
        tl = Time_load()  
        tl.webpage_wait()    
        for url in self.urls:
            req = tl.request(url)
            if req['data']["successfulFVRuns"] >= 1:
                


            


                    
                    




        


