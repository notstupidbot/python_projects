#!/usr/bin/env python3
import sys
import os


sys.path.append(os.path.realpath('%s/..' % os.path.dirname(__file__)))

from robots.fn import errors, log, lang,  pq, dict2htmTable, RED,GREEN,BLUE,RESET,BLACK,WHITE
from robots.datasource import DataSource
from config.cli_config import cli_config, db_path, cookie_path,browser_cache_dir
from api.course import CourseApi, isLinkedinLearningUrl
import validators
import re
import time
# from tabulate import tabulate


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage   : ./api_test.py <course_url>")
        print("example : ./api_test.py https://www.linkedin.com/learning/learning-next-js")
        sys.exit()
    course_url = sys.argv[1]
    if not validators.url(course_url):
        print(f"{course_url} is not a valid url")
        sys.exit()
    
    if not isLinkedinLearningUrl(course_url):
        print(f"{course_url} is not a valid linkedin learning url")
        sys.exit()
    
    ds = DataSource(db_path)
    api_course=CourseApi(ds)

    course_slug = api_course.getCourseSlugFromUrl(course_url)
    course = api_course.getCourseInfo(course_slug)

    if course:
        # course_dict=course.__dict__
        # course_dict.pop('_sa_instance_state')
        print(course)
        # sys.exit()
    else:
        sys.exit()
    sections = api_course.getCourseSections(course_slug)
    if sections:
        print(sections)
    else:
        sys.exit()
    tocs = api_course.getCourseTocs(course_slug)

    for section in sections:
        toc_list = tocs[section.slug]
        # setream_locations = api_course.getStreamLocs(toc.item_star)
        for toc in toc_list:
            # lst = "%s,%s,%s" % (toc.url, toc.item_star,toc.v_status_urn)
            # if toc.slug == "data-types-in-sql":
                #     stream_locs=api_course.getStreamLocs(toc)
                # print(stream_locs)
                stream_locations = api_course.getStreamLocs(toc)
                print(stream_locations)
                transcripts = api_course.getTranscripts(toc)
                print(transcripts)