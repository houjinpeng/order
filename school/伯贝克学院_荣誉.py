import requests
import time
from pymysql import connect
import re
from lxml import etree
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s -line:%(lineno)d - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

conn = connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test', charset='utf8')
cursor = conn.cursor()

class School():
    def __init__(self):
        self.school_name = 'Birkbeck University of London'
        self.school_url = 'https://www.bbk.ac.uk'
        self.domain = 'https://www.bbk.ac.uk'
        self.url = 'https://www.bbk.ac.uk/departments'
        self.headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': "max-age=0",
            'Connection': "keep-alive",
            'Host': "www.bbk.ac.uk",
            'Referer': "https://www.bbk.ac.uk/",
            'sec-ch-ua-mobile': "?0",
            'Sec-Fetch-Dest': "document",
            'Sec-Fetch-Mode': "navigate",
            'Sec-Fetch-Site': "same-origin",
            'Sec-Fetch-User': "?1",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }

    def request_handler(self, url):
        try:
            r = requests.get(url,headers=self.headers,timeout=10)
            return r
        except Exception as e:
            time.sleep(1)
            logger.info(url)
            return self.request_handler(url)

    def parse_academy(self,r):
        e = etree.HTML(r.text)
        academy_dict = {}
        academy_data = e.xpath('//div[@id="content"]//div[@class="row"]')
        for i in range(1,len(academy_data)-1,2):
            academy_url = academy_data[i].xpath('.//a[@class="internal-link"]/@href')[0]
            academy = academy_data[i].xpath('.//a[@class="internal-link"]//text()')[0]
            department_data = academy_data[i+1].xpath('.//div[@class="column medium-3 "]')
            academy_dict[academy] = []
            for department in department_data:
                department_dict = {}
                try:
                    department_dict['academy'] = academy
                    department_dict['academy_url'] = academy_url
                    if 'http' in department.xpath('.//a[@class="card "]/@href')[0]:
                        continue
                    department_dict['department_url'] = self.domain +department.xpath('.//a[@class="card "]/@href')[0]
                    department_dict['department'] =department.xpath('.//h3[@class="card__title  "]//text()')[0]
                except Exception as e:
                    # logger.info(e)
                    pass
                academy_dict[department_dict['academy']].append(department_dict)
            # logger.info(academy_dict)
        return  academy_dict

    def parse_people(self,r,teacher_dict):
        r_e = etree.HTML(r.text)
        # title_list = r_e.xpath('//div[@class="plain"]/div/h3')
        # ul_list = r_e.xpath('//div[@class="plain"]/div/ul')
        ul_list = r_e.xpath('//div[@class="plain"]/ul')
        for ul in ul_list[:-1]:
            href = ul.xpath('.//li/a/@href')
            if href != []:
                if 'our-staff/profile' in href[0]:
                    continue
                for li in ul.xpath('./li'):
                    peo = li.xpath('.//text()')[0]
                    name_f = peo.split(':')
                    teacher_dict['name'] = name_f[0]
                    try:
                        teacher_dict['professional'] = name_f[1]
                    except Exception:
                        teacher_dict['professional'] = ''
                    self.parse_detail(teacher_dict)

                # print(ul)


        # all_peo = e.xpath('//*[@id="content"]/div[2]/div/div/ul[1]/li//text()')
        # #荣誉人员
        # p_l = re.findall('(<h3.*?</h3>.*?)<h3', r.text, re.S)
        # if p_l != []:
        #     for p in p_l:
        #         if 'our-staff/profile' in p:
        #             continue
        #         e = etree.HTML(p)
        #         # peo_list = etree.HTML(r[0]).xpath('.//ul')
        #         peo_list = e.xpath('.//ul[@class="content-pull-down"]/li//text()')
        #         for peo in peo_list:
        #             # name = etree.HTML(r[0]).xpath('.//strong/text()')
        #             name_f = peo.split(':')
        #             teacher_dict['name'] = name_f[0]
        #             try:
        #                 teacher_dict['professional'] = name_f[1]
        #             except Exception:
        #                 teacher_dict['professional'] = ''
        #
        #
        #             self.parse_detail(teacher_dict)





    def parse_detail(self,teacher_dict):

        name =teacher_dict['name']
        school = self.school_name
        school_url = self.school_url
        academy = teacher_dict['academy'].replace('School of ','')
        academy_url =  teacher_dict['academy_url']
        list_url = teacher_dict['list_url']
        institute = ''  #机构/研究院 三级部门
        department = teacher_dict['department'].replace(',',' ')
        professional = teacher_dict['professional'] #职称

        header_img = ''

        email = ''
        phone = ''

        research_direction = '' #研究方向
        subject = ''
        work_experience = ''
        representative_work = ''
        award = ''
        project = ''
        teach = ''
        supervise_stutent = ''
        social_appointments = ''

        flag = teacher_dict['professional'] #标签
        mainurl = ''#详情地址
        try:
            content = etree.tostring(e.xpath('//div[@class="column medium-10 large-8"]')[0],encoding='utf-8').decode()
        except Exception as e:
            # logger.info(e)
            content = ''
        unit = ''

        sql = f'INSERT INTO talent_info (`name`,school,school_url,academy,academy_url,list_url,institute,department,professional,header_img,email,phone,research_direction,`subject`,work_experience,representative_work,award,project,teach,supervise_stutent,social_appointments,flag,mainurl,content,unit) values ' \
              f'("{name}","{school}","{school_url}","{academy}","{academy_url}","{list_url}","{institute}","{department}","{professional}","{header_img}","{email}","{phone}","{research_direction}","{subject}","{work_experience}","{representative_work}","{award}","{project}","{teach}","{supervise_stutent}","{social_appointments}","{flag}","{mainurl}","{conn.escape_string(content)}","{unit}")'
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            logger.info(sql)
        logger.info(f'名字:{name} 学校:{school} 学校链接:{school_url} 学院:{academy} 学院链接:{academy_url} 人员列表:{list_url} 系:{institute}  职称:{professional}  头像:{header_img} 邮件:{email} 电话:{phone} 标签:{flag} 详情链接:{mainurl}')

    def index(self):
        r = self.request_handler(self.url)
        academy_dict = self.parse_academy(r)
        for key,value in academy_dict.items():
            for v in value:
                # logger.info(v)
                try:
                    list_url = v['department_url']+'our-staff'
                    list_resp = self.request_handler(list_url)
                    v['list_url'] = list_url
                    self.parse_people(list_resp,v)
                except Exception as e:
                    pass




School().index()
