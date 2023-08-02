#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.realpath('%s/..' % os.path.dirname(__file__)))

from robots.fn import errors, log, lang,  pq, dict2htmTable, RED,GREEN,BLUE,RESET,BLACK,WHITE
from robots.datasource import DataSource
from config.cli_config import cli_config, db_path, cookie_path,browser_cache_dir,download_dir
from api.course import CourseApi, isLinkedinLearningUrl,isTimeExpired,downloadFile,getDownloadDir
import validators
import re
import time

def getAttr(obj,key):
    try:
        return getattr(obj,key)
    except Exception as e:
        print(e)
    return None

def download(args):
    print(args)
    course_id = getAttr(args,'id')
    run = getAttr(args,'run')
    section_id = getAttr(args,'section_id')
    toc_id = getAttr(args,'toc_id')
    transcript_lang = getAttr(args,'transcript_lang')
    transcript_only=getAttr(args,'transcript_only')
    fmt=getAttr(args,'fmt')

    ds = DataSource(db_path)
    api_course=CourseApi(ds)
    course_list = ds.m_course.getList()
    download_mode="course_mode"
    download_transcript=False
    
    if run:
        # if course_id:
        #     print(f"course id : {course_id}")
        
        if toc_id:
            # print(f"toc id : {toc_id}")
            download_mode="toc_mode"
            if section_id or course_id:
                log('Option ignored -i|--id or -si|--section-id, if you have specify -ti|--toc-id')
        elif section_id:
            download_mode="section_mode"
            if course_id:
             log('Option ignored -i|--id , if you have specify -si|--section-id')
        # if transcript_lang:
        #     print(f"transcript lang : {transcript_lang}")

        print("Download manager is running")
        if transcript_only:
            if not transcript_lang:
                errors("You must specify -tl|--transcript-lang, example -tl en", exit_progs=True)
        
        if not fmt:
                errors("You must specify -f|--fmt, example -f 720", exit_progs=True)

        if download_mode == "course_mode":
            pass
        if download_mode == "section_mode":
            log('Download in section mode')
            section = ds.m_section.get(section_id)
            if not section:
                errors(f"Section with id: {section_id} not found")
            course = ds.m_course.get(section.courseId)
            print(f"Section title: {section.title} , Course : {course.title}")
            print(f"Selected fmt: {fmt}")
            print(f"Selected transcript lang: {transcript_lang}")
            availableFmt = ds.m_course.getAvailableStreamFmt(section.courseId)
            availableFmt_str=','.join(list(availableFmt))
            log(f"available fmt:[{availableFmt_str}]")
            log("Checking available fmt")
            if not fmt in availableFmt:
                errors(f"fmt : {fmt} is not available, valid fmt: {availableFmt_str}")
            else:
                log(f"fmt : {fmt} is Ok")
                
            if transcript_lang:
                availableTrans = ds.m_course.getAvailableTransLang(section.courseId)
                availableTrans_str=','.join(list(availableTrans))
                log(f"available transcript lang:[{availableTrans_str}]")
                if not transcript_lang in availableTrans:
                    errors(f"transcript lang : {transcript_lang} is not available, valid transcript lang: {availableTrans_str}")
                else:
                    log(f"transcript lang : {transcript_lang} is Ok")
            
            toc_number=1
            tocs = ds.m_toc.getListBySectionId(section.id)
            for toc in tocs:
                    stream_loc_keys = ""
                    stream_locs = ds.m_stream_location.getByTocId(toc.id)
                    if not stream_locs:
                        stream_locs = api_course.getStreamLocs(toc)
                    if stream_locs:
                        ok=False
                        wait_time=0
                        retry_count=0
                        max_retry_count=3
                        refresh_stream_locs=False
                        while not ok:
                            if wait_time > 0:
                                log(f"wait for {wait_time} seconds")
                                time.sleep(wait_time)
                            if retry_count > 0:
                                log(f"retry count : {retry_count}")
                            
                            if refresh_stream_locs:
                                log(f"refershing stream locs")
                                stream_locs = api_course.getStreamLocs(toc,refresh=True)

                            print(f"{stream_locs[fmt]}")


                            download_dir = getDownloadDir(course.slug)
                            media_output_filename = f"{download_dir}/{toc.slug}-{fmt}.mp4"
                            # print(media_output_filename)
                            url=stream_locs[fmt].url
                            status_code = downloadFile(url,media_output_filename)
                            if status_code != 200:
                                retry_count += 1
                                wait_time += 5
                                
                                if status_code == 401:
                                    refresh_stream_locs=True

                                if retry_count > max_retry_count:
                                    errors(f"Max retry count exceed max : {max_retry_count}")
                                    ok=True
                            else:
                                ok=True


            pass
        if download_mode == "toc_mode":
            pass
        if download_mode == "course_mode":
            pass
        # if download_mode == "transcript_mode":
        #     log('Download in transcript mode')
        #     pass
        sys.exit()
    # print(course_list)
    if not course_id:
        print("\nList of saved courses:\n")
        for course in course_list:
            by_authors=[]
            for author in course.authors:
                by_authors.append(author.name)
            sloc_fmt = ds.m_course.getAvailableStreamFmt(course.id)
            # print(sloc_fmt)   
            trans_lang = ds.m_course.getAvailableTransLang(course.id)
            # print(trans_lang)    
            print(f"  [{GREEN}i{RESET}:{RED}{course.id}{RESET}]. {course.title} By {','.join(by_authors)}")
            print(f"     Available fmt [{GREEN}f{RESET}:{RED}{','.join(sloc_fmt)}{RESET}]")
            print(f"     Available transcript lang [{GREEN}tl{RESET}:{RED}{','.join(trans_lang)}{RESET}]\n")
        # print("\n")
        print("  description:\n")
        print(f"    {GREEN}i{RESET}  : {RED}Course id{RESET}")
        print(f"    {GREEN}f{RESET}  : {RED}Media format{RESET}")
        print(f"    {GREEN}tl{RESET} : {RED}Transcript lang{RESET}\n")
    else:
        course = ds.m_course.get(course_id)
        if not course:
            errors(f"Course with id {course_id} not found.", exit_progs=True)
        
        output_buffer = f"\n\n {course.title}"
        by_authors=[]
        for author in course.authors:
            by_authors.append(author.name)
        output_buffer += f"\n By {','.join(by_authors)}\n"

        sections = ds.m_section.getListCourseId(course_id)
        # section_number = 1
        for section in sections:
            output_buffer += f"\n\n  [{GREEN}si{RESET}:{section.id}] {section.title}\n"
            toc_number=1
            tocs = ds.m_toc.getListBySectionId(section.id)
            for toc in tocs:
                stream_loc_keys = ""
                stream_locs = ds.m_stream_location.getByTocId(toc.id)
                if not stream_locs:
                    stream_locs = api_course.getStreamLocs(toc)
                if stream_locs:
                    stream_loc_keys = list(stream_locs)
                    if len(stream_loc_keys)>0:
                        stream_loc_keys = f"[{GREEN}f{RESET}:{RED}{','.join(stream_loc_keys)}{RESET}]"
                    else:
                        stream_loc_keys = ""
                
                transcript_keys = ""
                transcripts = ds.m_transcript.getByTocId(toc.id)
                if not transcripts:
                    transcripts = api_course.getTranscripts(toc)
                if transcripts:
                    transcript_keys = list(transcripts)
                    if len(transcript_keys)>0:
                        transcript_keys = f"[{GREEN}tl{RESET}:{RED}{','.join(transcript_keys)}{RESET}]"
                    else:
                        transcript_keys = ""
                # toc_id = "ti:%d" % toc.id
                output_buffer += f"\n    [{GREEN}ti{RESET}:{toc.id}] {toc_number}. {toc.title} {stream_loc_keys} {transcript_keys}"
                toc_number += 1
            # section_number += 1

        print(f"{output_buffer}\n")
        print("\n  description:\n")
        print(f"    {GREEN}si{RESET} : Section id")
        print(f"    {GREEN}ti{RESET} : Toc id\n")
