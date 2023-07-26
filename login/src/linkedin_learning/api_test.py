#!/usr/bin/env python3
from robots import Page, Human, JsonConfig
# from robots.pages import unauthenticated_page,authenticated_page,login_email_page, login_passwd_page, login_pin_page, login_library_page, login_library_card_page
from robots.fn import errors, log, lang, waitForCaptcha, inputAction,cleanQueryString, pq, writeFile
from robots.config import linkedin_learning_url
import login_individual
import login_library
import sys
from robots.datasource import DataSource
from api.course import fetchCourseUrl
from prx import Prx
import json
import re
import xmltodict

def parseJson(code_id,code_nd):
    code_content=""
    try:
        code_content=json.loads(code_nd.text())
    except Exception as e:
        errors('error parsing %s' % code_id,e)
    
    return code_content
######################################################
#JsonConfig
######################################################
# json_config=JsonConfig(path="myconfig.json")
# waitForCaptcha(json_config)
#######################################################
# Darabase settings
######################################################
# db_setting_key="db_path"
# db_path="my.db"
# if not json_config.get(db_setting_key):
#     json_config.set(db_setting_key, db_path)

# ds = DataSource(db_path)
# sys.exit()
######################################################
# MIMIC HUMAN
######################################################
human = Human()

course_url="https://www.linkedin.com/learning/learning-next-js?u=95231473"
course_url="https://www.linkedin.com/learning/creating-fun-and-engaging-video-training-the-how"
course_url=cleanQueryString(course_url)

prx=Prx(human)
print(course_url)
content=prx.get(course_url)
# print(content)
# sys.exit()
doc=pq(content)
codes=doc("code")
codes_dict = {}



data={"root":{}}

for code in codes:
    code_nd = pq(code)
    code_id=code_nd.attr('id')
    # capture id as key values
    key = None
    pattern = r'\d+$'
    # Use re.search to find the number at the end of the string
    match = re.search(pattern, code_id)
    if match:
        id =  match.group()
        prop = code_id.replace('-%s' % id,'')
        id = "item_%s" % id
        if not id in data["root"]:
            data["root"][id] = {}

        if prop == "datalet-bpr-guid":
            if not 'key' in data["root"][id]:
                data["root"][id]['key'] = parseJson(code_id, code_nd)
        elif prop == "bpr-guid":
            if not 'value' in data["root"][id]:
                data["root"][id]['value'] = parseJson(code_id, code_nd)


xml_data = xmltodict.unparse(data, pretty=True).replace('<body','<tbody').replace('</body','</tbody').replace('<$','<').replace('</$','</').replace('<*','<star-').replace('</*','</star-')
page_name = 'course_data'
xml_path = 'html_cache/%s.xml' % page_name
writeFile(xml_path, xml_data)
data = open(xml_path, 'rb')

xslt_content = data.read()
doc=pq(xslt_content)

def getCourseInfo(doc):
    rq_coure_nd=doc('request:contains("/learning-api/courses")')
    rq_coure_nd_p = rq_coure_nd.parent()
    tbody=rq_coure_nd_p('tbody').text()
    match = re.search(pattern, tbody)
    item_key='item_%s' % match.group()
    root_el = doc("%s > value > data" % item_key)
    course_urn=root_el("star-elements").text()
    entity_urn = doc('entityUrn:contains("%s")' % course_urn)
    if len(entity_urn)>0:
        for nd in entity_urn:
            nd = doc(nd)
            if nd.text() == course_urn:
                p = nd.parent()
                data={
                    "title" : p('title').text(),
                    "slug" : p('slug').text(),
                    "descriptionv2" : p('descriptionv2 > text').text(),
                    "descriptionV3" : p('descriptionV3 > text').text(),
                    "exerciseFiles" : {},
                    "sourceCodeRepository": p('sourcecoderepository').text(),
                    "duration" : p('duration>duration').text(),
                    "dificulty": p('difficultylevel').text(),
                    "viewerCounts" : p('viewercounts > total').text(),
                    "visibility" : p('visibility').text()
                }
                tags = ["sizeInBytes","name","url"]
                for tag in tags:
                    exercise_file_nd = p('exerciseFiles > %s' % tag) 
                    data["exerciseFiles"][tag]=exercise_file_nd.text()
                
                # primarythumbnailv2
                # features > contentrating
                # urn star
                #   authors
                #   contents
                #  authorsv2

                print(data)


    # print(item_key)

getCourseInfo(doc)