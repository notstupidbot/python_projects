#!/usr/bin/env python3
import sys
from api.course import fetchCourseUrl, getCourseInfo
from robots.fn import errors, log, lang,  pq, dict2htmTable


course_url="https://www.linkedin.com/learning/learning-next-js?u=95231473"
# course_url="https://www.linkedin.com/learning/creating-fun-and-engaging-video-training-the-how"

xml_doc = fetchCourseUrl(course_url)
course_info=getCourseInfo(xml_doc)
course_info_tbl=dict2htmTable(course_info)
print(course_info_tbl)