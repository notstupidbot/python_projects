#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.realpath('%s/..' % os.path.dirname(__file__)))

from robots.fn import errors, log, lang,  pq, dict2htmTable, RED,GREEN,BLUE,RESET,BLACK,WHITE
from robots.datasource import DataSource
from config.cli_config import cli_config, db_path, cookie_path,browser_cache_dir
from api.course import fetchCourseUrl, getCourseInfo, fetchCourseTocUrl, getCourseToc,getVideoMeta
import validators
import re

def is_linkedin_learning_url(url):
    pattern = r'^https://www\.linkedin\.com/learning/'
    return re.match(pattern, url) is not None


ds = DataSource(db_path)
db_config=ds.mConfig
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage   : ./api_test.py <course_url>")
        print("example : ./api_test.py https://www.linkedin.com/learning/learning-next-js")
        sys.exit()
    course_url = sys.argv[1]
    if not validators.url(course_url):
        errors(f"{course_url} is not a valid url")
        sys.exit()
    
    if not is_linkedin_learning_url(course_url):
        errors(f"{course_url} is not a valid linkedin learning url")
        sys.exit()

    log("Getting course info sections, tocs, stream locs and transcripts")
    # course_url="https://www.linkedin.com/learning/learning-next-js?u=95231473"
    # course_url="https://www.linkedin.com/learning/creating-fun-and-engaging-video-training-the-how"
    try:
        xml_doc = fetchCourseUrl(course_url)
    except Exception as e:
        errors('could_not_fetch_course_url',e)
        sys.exit(1)
    if xml_doc:    
        course_info=getCourseInfo(xml_doc,db_config)
    else:
        errors('could_not_parse_xml_doc')
        sys.exit(1)
    # course_info_tbl=dict2htmTable(course_info)
    # print(course_info_tbl)
    # print(course_info)
    if not course_info:
        errors('could_not_get_course_info')
        sys.exit(1)
    output_buffer = "\n"
    output_buffer += course_info["title"]+"\n\n"
    output_buffer += course_info["description"]+"\n\n"
    # output_buffer=""
    # print(course_info["slug"])
    # course_url = "%s/%s" % (linkedin_learning_url, course_info["slug"])
    # print(course_info["url"])
    if course_info["sections"]:
        for section_slug in course_info["sections"]:
            section = course_info["sections"][section_slug]
            output_buffer += "\n  "+section["title"]+"\n"

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
                            if not toc["stream_locations"] or not toc["transcripts"]:
                                log(lang('try_to_fetch_course_toc', toc['url']))
                                xml_doc = fetchCourseTocUrl(toc['url'])
                                # json_config = JsonConfig(path=f"{course_slug}.json")

                                stream_locations, transcripts = getVideoMeta(toc["v_status_urn"], xml_doc,db_config)
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
                            stream_loc_list = ','.join(list(toc["stream_locations"]))
                            stream_location_keys = f"{GREEN}[{stream_loc_list}]{RESET}"
                        transcript_keys = ""
                        if toc["transcripts"]:
                            has_transcripts = True
                            transcript_list = ','.join(list(toc["transcripts"]))
                            transcript_keys = f"{BLUE}[{transcript_list}]{RESET}"
                        COLOR = BLACK    
                        if has_stream_locations and has_transcripts:
                            COLOR = GREEN  
                        elif has_transcripts:
                            COLOR = BLUE
                        elif toc["visibility"]=="LOCKED":
                            COLOR = WHITE
                        else:
                            COLOR=BLACK  
                        toc_title = toc["title"]
                        output_buffer += f"\t{COLOR}{index}.{toc_title}{RESET} {stream_location_keys} {transcript_keys}\n"
                        index+=1
output_buffer += "\n" 
print(output_buffer)