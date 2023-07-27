#!/usr/bin/env python3
import sys
from api.course import fetchCourseUrl, getCourseInfo, fetchCourseTocUrl, getCourseToc,getVideoMeta
from robots.fn import errors, log, lang,  pq, dict2htmTable, RED,GREEN,BLUE,RESET,BLACK,WHITE
from robots.json_config import JsonConfig
import logging

import logging
import dicttoxml

dicttoxml.LOG.setLevel(logging.ERROR)
logger = logging.getLogger("dicttoxml")
logger.setLevel(logging.ERROR)
if __name__ == '__main__':


    logger.disabled = True
    # logging.disable(1)

    # logging.basicConfig(
    # format="%(levelname) -10s %(asctime)s %(filename)s:%(lineno)s  %(message)s",
    # level=logging.NOTSET)

    # logging.getLogger().disabled = True  # True, False

    # logging.critical("Critical")
    # logging.error("Error")
    # logging.warning("Warning")
    # logging.info("Info")
    # logging.debug("Debug")

    course_url="https://www.linkedin.com/learning/learning-next-js?u=95231473"
    # course_url="https://www.linkedin.com/learning/creating-fun-and-engaging-video-training-the-how"
    try:
        xml_doc = fetchCourseUrl(course_url)
    except Exception as e:
        errors('could_not_fetch_course_url',e)
        sys.exit(1)
    if xml_doc:    
        course_info=getCourseInfo(xml_doc)
    else:
        errors('could_not_parse_xml_doc')
        sys.exit(1)
    # course_info_tbl=dict2htmTable(course_info)
    # print(course_info_tbl)
    print(course_info)
    if not course_info:
        errors('could_not_get_course_info')
        sys.exit(1)
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
                        course_slug = course_info["slug"]    
                        if toc["visibility"]!="LOCKED":
                            log(lang('try_to_fetch_course_toc', toc['url']))
                            xml_doc = fetchCourseTocUrl(toc['url'])
                            json_config = JsonConfig(path=f"{course_slug}.json")

                            stream_locations, transcripts = getVideoMeta(toc["v_status_urn"], xml_doc,json_config)
                            if stream_locations:
                                toc["stream_locations"]=stream_locations
                            else:
                                errors(lang('could_not_fetch_stream_locs'))    
                            if transcripts:
                                toc["transcripts"]=transcripts
                            else:
                                errors(lang('could_not_fetch_transcripts'))    


                
                            # break
                        # print("\t"+toc["url"])
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
                        elif toc["visibility"]=="LOCKED":
                            COLOR = WHITE
                        else:
                            COLOR=BLACK  
                        print(COLOR + ("\t%2d. "% index)+toc["title"] + RESET+ stream_location_keys + transcript_keys )
                        index+=1
                        
            print("\n")