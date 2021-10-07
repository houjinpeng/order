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
        # all_peo = e.xpath('//ul[@class="content-pull-down"]')[1].xpath('./li')
        all_peo = re.findall('https{0,1}?://www.bbk.ac.uk/our-staff/profile/\d+/.*?"', r.text)
        # all_peo =  all_peo+all_peo1
        for peo in all_peo:
            # teacher_dict['name'] =  peo.xpath('.//a/text()')[0]
            # teacher_dict['mainurl'] =  peo.xpath('.//a/@href')[0]
            teacher_dict['mainurl'] =  peo
            # print(peo)
            # logger.info(teacher_dict['mainurl'])
            r = self.request_handler(teacher_dict['mainurl'])
            self.parse_detail(r,teacher_dict)

    def parse_detail(self,r,teacher_dict):
        e = etree.HTML(r.text)
        # name = teacher_dict['name']
        name = e.xpath('//h1/text()')[0].replace('\n ','').replace('  ','').strip()
        school = self.school_name
        school_url = self.school_url
        academy = teacher_dict['academy'].replace('School of ','')
        academy_url =  teacher_dict['academy_url']
        list_url = teacher_dict['list_url']
        institute = teacher_dict['department']  #机构/研究院 三级部门
        department = ''
        professional = ''.join(e.xpath('//li[@class="primary-typeface"]/text()')).strip().replace('\n','').replace('  ','').replace(institute,'') #职称
        if professional.strip()[-1] == ',':
            professional = professional.strip()[:-1]
        try:
            header_img = ''.join(e.xpath('//div[@class="column small-3 medium-4"]/img/@data-srcset')).split(',')[-1].strip().split(' ')[0]
        except Exception:
            header_img = ''.join(e.xpath('//div[@class="column small-3 medium-4"]/img/@src'))   #头像
        email = re.findall('href="mailto:(.*?)"',r.text)
        if email == []:
            email = ''
        else:
            email = email[0]
        phone = re.findall('href="tel:(.*?)"',r.text)
        if phone == []:
            phone = ''
        else:
            phone = phone[0]
        if phone == '+442076316000':
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

        flag = professional #标签
        mainurl = r.url#详情地址
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
                    list_url = v['department_url']+'/our-staff'
                    list_resp = self.request_handler(list_url)
                    v['list_url'] = list_url
                    self.parse_people(list_resp,v)
                except Exception as e:
                    logger.error(e)
                    pass




School().index()
