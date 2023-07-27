#!/usr/bin/env python3
import sys
from api.course import fetchCourseUrl, getCourseInfo
from robots.fn import errors, log, lang,  pq, dict2htmTable, RED,GREEN,BLUE,RESET,BLACK,WHITE


course_url="https://www.linkedin.com/learning/learning-next-js?u=95231473"
# course_url="https://www.linkedin.com/learning/creating-fun-and-engaging-video-training-the-how"

xml_doc = fetchCourseUrl(course_url)
course_info=getCourseInfo(xml_doc)
# course_info_tbl=dict2htmTable(course_info)
# print(course_info_tbl)
print("\n")
print(course_info["title"]+"\n")
# print(course_info["slug"])
# course_url = "%s/%s" % (linkedin_learning_url, course_info["slug"])
# print(course_info["url"])
if course_info["sections"]:
    for section_slug in course_info["sections"]:
        section = course_info["sections"][section_slug]
        print("  "+section["title"]+"\n")

        if course_info["tocs"]:
            if course_info["tocs"][section_slug]:
                index = 1
                for toc in course_info["tocs"][section_slug]:
                    # toc = course_info["tocs"][section_slug][toc_slug]
                    stream_location_keys = ""
                    has_stream_locations = False
                    has_transcripts = False
                    if toc["stream_locations"]:
                        has_stream_locations = True
                        stream_location_keys = GREEN+" ["+','.join(list(toc["stream_locations"]))+"]"+RESET
                    transcript_keys = ""
                    if toc["transcripts"]:
                        has_transcripts = True
                        transcript_keys = BLUE+" ["+','.join(list(toc["transcripts"]))+"]"+RESET
                    COLOR = BLACK    
                    if has_stream_locations and has_transcripts:
                        COLOR = GREEN  
                    elif has_transcripts:
                        COLOR = BLUE
                    else:
                        COLOR=WHITE  
                    print(COLOR + ("\t%2d. "% index)+toc["title"] + RESET+ stream_location_keys + transcript_keys )
                    index+=1
                    # print("\t"+toc["url"])
        print("\n")