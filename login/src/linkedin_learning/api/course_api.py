from api.course_fn import parseJson,convert2Xml,parseRestLiResponse,isLinkedinLearningUrl,courseUrl,getCourseSlugFromUrl
from api.course_fn import getCourseTocs,getCourseSections,getCourseInfo,getCourseXmlParentElement,getVideoMeta
from api.course_fn import getStreamLocations
from robots.fn import benchmark, errors, log, lang
from api.prx import Prx
from bs4 import BeautifulSoup
import time
class DictToObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)

def getVideoMetaNd(v_status_urn, doc):
    benchmark('getVideoMetaNd','start')
    v_meta_data_nd=None
    # cache = json_config.get(v_status_urn)
    # if cache:
    #     log(lang('get_video_meta_from_cache',v_status_urn), verbose=True)
    #     b=benchmark('getVideoMeta','end')
    #     print(f"getVideoMeta time elapsed:{b['elapsed_time']}\n")
    #     return [cache[0],cache[1],777]
    # print(v_status_urn)

    # urn:li:lyndaVideoViewingStatus:urn:li:lyndaVideo:(urn:li:lyndaCourse:2491193,3099399)
    # urn:li:lyndaVideoViewingStatus:urn:li:lyndaVideo:(urn:li:lyndaCourse:2491193,3094437)
    v_status_lookups = doc.find_all('star_lyndaVideoViewingStatus',text=v_status_urn)
    # v_status_lookups = doc.find_all('included')
    status_429 = doc.find_all('status',text="429")
    status_els= doc.find_all('status')
    # print(statuses)
    # status=427
    statuses=[]
    for status_el in status_els:
        statuses.append(int(status_el.text))

    # print(len(status_429))
    # print(v_status_lookups)

    if not v_status_lookups:
        errors('A')
        errors(lang('could_not_find_v_status_lookup', v_status_urn))

        v_status_urn = v_status_urn.replace('urn:li:lyndaVideoViewingStatus:','')
        v_status_lookups= doc.find_all('trackingUrn', text=v_status_urn)
    
    if not v_status_lookups:
        errors('B')
        errors(lang('could_not_find_v_status_lookup', v_status_urn))
    # print(v_status_lookup)
    stream_locations = None
    transcripts = None
    # print(v_status_lookup)

    v_status_lookup=None
    v_meta_data_nd=None
    pos=-1
    if v_status_lookups:
        # print(v_status_lookup)

        break_the_loop=False
        for v_status_lookup in v_status_lookups:
            el_nd = v_status_lookup.parent 
            # parent_el = el_nd("parent")
            v_meta_data_nd = el_nd.find("presentation")
            pos=0
            if v_meta_data_nd:
                pos += 1
                v_meta_data_nd = v_meta_data_nd.find("videoPlay")
                if v_meta_data_nd:
                    pos += 1
                    v_meta_data_nd = v_meta_data_nd.find("videoPlayMetadata")
                    break_the_loop=True 
                        
            if break_the_loop:
                break
    if not v_meta_data_nd:
        # print(v_status_lookup)
        errors("%s %s" % (lang('could_not_find_v_meta_data_nd_pos'),pos))
    b=benchmark('getVideoMetaNd','end')
    print(f"getVideoMetaNd time elapsed:{b['elapsed_time']}\n")  
    return [v_meta_data_nd,statuses]

def inArray(item, lsts):
    item_index= -1
    try:
        index = lsts.index(item)
        item_index=index
    except ValueError:
        pass
    return item_index
class CourseApi:
    ds=None
    human=None
    m_course=None
    m_config=None
    m_exercise_file=None
    m_section=None
    course=None
    
    def __init__(self, ds):
        self.ds = ds
        self.m_config = ds.m_config
        self.m_course = ds.m_course
        self.m_section = ds.m_section
        self.m_exercise_file=ds.m_exercise_file
        self.course_xml_doc=None
        self.toc_xml_doc={}
        self.m_toc = ds.m_toc
        self.m_prx = ds.m_prx
        self.m_stream_location = ds.m_stream_location
    
    def getCourseSlugFromUrl(self,url):
        course_slug,toc_slug=getCourseSlugFromUrl(url)
        return course_slug
    
    def getCourseInfo(self, course_slug):
        benchmark('ApiCourse.getCourseInfo','start')

        course = self.m_course.getBySlug(course_slug)
        if not course:
            course = self.fetchCourseInfo(course_slug)
        b=benchmark('ApiCourse.getCourseInfo','end')
        print(f"ApiCourse.getCourseInfo time elapsed:{b['elapsed_time']}\n")
        self.course = course
        return course
    
    def getCourseXmlDoc(self,course_url, no_cache=False):
        if not self.course_xml_doc:
            prx=Prx(m_prx=self.m_prx)
            content=prx.get(course_url, no_cache)
            if content:
                page_name=prx.getPageName()
                doc=BeautifulSoup(content,features='html.parser')
                data=parseRestLiResponse(doc)
                self.course_xml_doc=convert2Xml(data, page_name)
        return self.course_xml_doc

    def fetchCourseInfo(self, course_slug):

        course=None
        course_url = courseUrl(course_slug)
        xml_doc=self.getCourseXmlDoc(course_url, no_cache=True)
        if xml_doc:
            course = getCourseInfo(xml_doc)
            if course:
                rec=self.m_course.create(course["title"], course["slug"], course["duration"], course["sourceCodeRepository"], course["description"], course["urn"])
                if course["exerciseFiles"]:
                    sizeInBytes,name,url,=course["exerciseFiles"].values()
                    self.m_exercise_file.create(name=name,size=sizeInBytes,url=url,courseId=rec.id)
                course=rec
        return course

    def getCourseSections(self, course_slug):
        benchmark('ApiCourse.getCourseSections','start')

        course=None
        course_url = courseUrl(course_slug)
        xml_doc=self.getCourseXmlDoc(course_url)
        p,course_urn = getCourseXmlParentElement(xml_doc)
        sections = getCourseSections(p, xml_doc, self.m_section, self.course.id)
        self.sections = sections
        b=benchmark('ApiCourse.getCourseSections','end')
        print(f"ApiCourse.getCourseSections time elapsed:{b['elapsed_time']}\n")

        return sections
    
    def getCourseTocs(self, course_slug):
        benchmark('ApiCourse.getCourseTocs','start')

        tocs=None
        course_url = courseUrl(course_slug)
        xml_doc=self.getCourseXmlDoc(course_url)
        p,course_urn = getCourseXmlParentElement(xml_doc)
        sections = self.sections
        if not sections:
            sections = getCourseSections(p, xml_doc, self.m_section, self.course.id)
        if sections:    
            tocs = getCourseTocs(p, xml_doc, sections, self.m_toc, self.course.slug)

        b=benchmark('ApiCourse.getCourseTocs','end')
        print(f"ApiCourse.getCourseTocs time elapsed:{b['elapsed_time']}\n")

        return tocs
    
    def getStreamLocs(self, toc):
        benchmark('ApiCourse.getStreamLocs','start')

        #toc.url, toc.item_star,toc.v_status_urn
        # lst = "%s,%s,%s" % (toc.url, toc.item_star,toc.v_status_urn)
        stream_locations=None
        status = 400
        ok=False
        no_cache=False
        retry_count = 0
        wait_time=0

        while not ok:
                
            if retry_count > 0:
                print(f"retry {retry_count}")
            if wait_time>0:
                print(f"wait for {wait_time} second")
                time.sleep(wait_time)

            stream_locations=self.m_stream_location.getByTocId(toc.id)
            if stream_locations:
                log('stream_locations_get_from_m_stream_location')
                break
            else:
                toc_xml_doc = self.getTocXmlDoc(toc.slug, toc.url,no_cache=no_cache)
                
                v_meta_data_nd,statuses=getVideoMetaNd(toc.v_status_urn, toc_xml_doc)
                stream_locations=getStreamLocations(v_meta_data_nd, toc_xml_doc,toc,self.m_stream_location)
                print(stream_locations)
                
                print(f"status={statuses}")
                
                if inArray(429,statuses)>0 or inArray(427,statuses)>0 or len(statuses) == 0:
                    retry_count += 1
                    no_cache=True
                    wait_time+=5
                else:
                    ok=True
                    wait_time=0
                    if stream_locations:
                        pass
                        # for fmt in stream_locations:
                        #     stream_loc=stream_locations[fmt]
                        #     stream_location = self.m_stream_location.create(toc.id, fmt, stream_loc["url"], stream_loc["expiresAt"])
                        #     print(stream_location)
                if retry_count > 3:
                    print(f"retry counts reached max : {retry_count}")
                    wait_time=0

                    break    
            # print(status)
        b=benchmark('ApiCourse.getStreamLocs','end')
        print(f"ApiCourse.getStreamLocs time elapsed:{b['elapsed_time']}\n")
        return stream_locations

    def getStreamLocsAndTranscripts(self, toc):
        benchmark('ApiCourse.getStreamLocsAndTranscripts','start')

        #toc.url, toc.item_star,toc.v_status_urn
        # lst = "%s,%s,%s" % (toc.url, toc.item_star,toc.v_status_urn)
        stream_locations=None
        transcripts=None
        status = 400
        ok=False
        no_cache=False
        retry_count = 0
        wait_time=0
        while not ok:
                
            if retry_count > 0:
                print(f"retry {retry_count}")
            if wait_time>0:
                print(f"wait for {wait_time} second")
                time.sleep(wait_time)
            toc_xml_doc = self.getTocXmlDoc(toc.slug, toc.url,no_cache=no_cache)
            stream_locations, transcripts, status=getVideoMeta(toc.v_status_urn, toc_xml_doc, self.m_config)
            print(f"status={status}")
            if not status or status == 429 or status == 427:
                retry_count += 1
                no_cache=True
                wait_time+=5
            else:
                ok=True
                wait_time=0
                if stream_locations:
                    for fmt in stream_locations:
                        stream_loc=stream_locations[fmt]
                        stream_location = self.m_stream_location.create(toc.id, fmt, stream_loc["url"], stream_loc["expiresAt"])
                        print(stream_location)
            if retry_count > 3:
                print(f"retry counts reached max : {retry_count}")
                wait_time=0

                break    
            # print(status)
        b=benchmark('ApiCourse.getStreamLocsAndTranscripts','end')
        print(f"ApiCourse.getStreamLocsAndTranscripts time elapsed:{b['elapsed_time']}\n")
        return [stream_locations, transcripts, status]
    
    def getTocXmlDoc(self,toc_slug, toc_url, no_cache=False):
        if not toc_slug in self.toc_xml_doc or no_cache:
            prx=Prx(m_prx=self.m_prx)
            content=prx.get(toc_url, no_cache=no_cache)
            if content:
                page_name=prx.getPageName()
                doc=BeautifulSoup(content,features='html.parser')
                data=parseRestLiResponse(doc)
                self.toc_xml_doc[toc_slug]=convert2Xml(data, page_name)
        return self.toc_xml_doc[toc_slug]

    def fetchCourseUrl(self, url):
        pass
    
    def fetchTocUrl(self, url):
        pass