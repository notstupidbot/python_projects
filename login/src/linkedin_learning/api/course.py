from robots import Human
from api.prx import Prx
import json
import re
import xmltodict
from robots.fn import errors, log, lang, cleanQueryString, pq, writeFile,slugify
from robots.config import linkedin_learning_url
from bs4 import BeautifulSoup
from robots.json_config import JsonConfig

def parseJson(code_id,code_nd):
    code_content=""
    try:
        code_content=json.loads(code_nd.text())
    except Exception as e:
        errors('error parsing %s' % code_id,e)
    
    return code_content

def convert2Xml(data, page_name):
    xml_data = xmltodict.unparse(data, pretty=True)
    xml_data = xml_data.replace('<body','<tbody').replace('</body','</tbody')
    xml_data = xml_data.replace('<$','<').replace('</$','</')
    xml_data = xml_data.replace('<*','<star_').replace('</*','</star_')

    # page_name = 'course_data'
    xml_path = 'html_cache/%s.xml' % page_name
    writeFile(xml_path, xml_data)
    data = open(xml_path, 'rb')

    xml_content = data.read()
    doc=BeautifulSoup(xml_content,features="xml")
    return doc

def parseRestLiResponse(doc):
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
    return data

def getTranscripts(v_meta_data_nd, doc):
    pg_transcript_nds = v_meta_data_nd.find_all("transcripts")
    transcripts=None
    tags = ["captionFormat","isAutogenerated","captionFile"] 
    # print(pg_transcript_nds)
    for pg_transcript_el in pg_transcript_nds:
        locale = pg_transcript_el.find("locale")
        if locale:
            
            lang = locale.find("language")
            if lang:
                lang = lang.text
                if not transcripts:
                    transcripts={}
                transcripts[lang] = {
                    "lang" : lang
                }
                country = locale.find("country")
                if country:
                    transcripts[lang]["country"] = country.text
                for tag in tags:
                    tag_nd = pg_transcript_el.find(tag)
                    if tag_nd:
                        transcripts[lang][tag] = tag_nd.text

    return transcripts
def getStreamLocations(v_meta_data_nd, doc):
    pg_stream_nds = v_meta_data_nd.find_all("progressiveStreams")
    stream_locations=None
    tags = ["size","bitRate","width","height"] 
    if pg_stream_nds:
        for pg_stream_el in pg_stream_nds:
            fmt = pg_stream_el.find("height")
            if fmt:
                fmt = fmt.text
                if not stream_locations:
                    stream_locations={}
                stream_locations[fmt] = {}
                stream_loc = pg_stream_el.find("streamingLocations")
                if stream_loc:
                    url = stream_loc.find("url")
                    if url:
                        url = url.text
                        stream_locations[fmt]["url"]=url
                    expiresAt = stream_loc.find("expiresAt")
                    if expiresAt:
                        expiresAt = expiresAt.text
                        stream_locations[fmt]["expiresAt"]=expiresAt

                    for tag in tags:
                        tag_nd = stream_loc.find(tag)
                        if tag_nd:
                            stream_locations[fmt][tag] = int(tag_nd.text) 

    return stream_locations
    # return None
def getVideoMeta(v_status_urn, doc, json_config):

    cache = json_config.get(v_status_urn)
    if cache:
        log(lang('get_video_meta_from_cache',v_status_urn), verbose=True)
        return cache
    # print(v_status_urn)

    # urn:li:lyndaVideoViewingStatus:urn:li:lyndaVideo:(urn:li:lyndaCourse:2491193,3099399)
    # urn:li:lyndaVideoViewingStatus:urn:li:lyndaVideo:(urn:li:lyndaCourse:2491193,3094437)
    v_status_lookups = doc.find_all('star_lyndaVideoViewingStatus',text=v_status_urn)
    if not v_status_lookups:
        v_status_urn = v_status_urn.replace('urn:li:lyndaVideoViewingStatus:','')
        v_status_lookups= doc.find_all('trackingUrn', text=v_status_urn)
    
    if not v_status_lookups:
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

                    if v_meta_data_nd:
                        pos += 1
                        stream_locations = getStreamLocations(v_meta_data_nd, doc)
                        transcripts = getTranscripts(v_meta_data_nd, doc)

                        if stream_locations and transcripts:
                            json_config.set(v_status_urn, [stream_locations,transcripts])
            if break_the_loop:
                break
    if not v_meta_data_nd:
        # print(v_status_lookup)
        errors("%s %s" % (lang('could_not_find_v_meta_data_nd_pos'),pos))
       
    return [stream_locations,transcripts]
def getCourseToc(item_star,doc,course_slug,json_config):
    

    toc_nd = doc.find('cachingKey',text=item_star)
    entity_urn=None
    if toc_nd:
        toc_nd_p = toc_nd.parent
        video_urn = toc_nd_p.find("content")
        if video_urn:
            video_urn = video_urn.find("video")
            if video_urn:
                video_urn = video_urn.text
                # print(video_urn)
                # break_the_loop=False
                entity_urn = doc.find('entityUrn',text=video_urn)
                if entity_urn:
                    toc={
                        "stream_locations" : None,
                        "transcripts" : None
                    }
                    entity_nd_p = entity_urn.parent
                    toc_slug = entity_nd_p.find("slug")
                    if toc_slug:
                        toc_slug = toc_slug.text
                        toc["slug"] = toc_slug
                        toc["url"] = "%s/%s/%s" % (linkedin_learning_url,course_slug,toc_slug)

                    
                    title = entity_nd_p.find("title")
                    if title:
                        title = title.text
                        toc["title"] = title

                    visibility = entity_nd_p.find("visibility") 
                    if visibility:
                        visibility = visibility.text
                        toc["visibility"] = visibility

                    duration = entity_nd_p.find("duration")
                    if duration:
                        duration = duration.find("duration")
                        if duration:
                            duration = duration.text
                            toc["duration"] = duration
                    v_status_urn = entity_nd_p.find("star_lyndaVideoViewingStatus")
                    if v_status_urn:
                        v_status_urn = v_status_urn.text
                        toc["v_status_urn"] = v_status_urn

                    stream_locations, transcripts = getVideoMeta(toc["v_status_urn"], doc, json_config)
                    if stream_locations:
                        toc["stream_locations"]=stream_locations
                    if transcripts:
                        toc["transcripts"]=transcripts
                    return toc
                
            if not entity_urn:
                errors(lang('could_not_find_video_entity_urn', item_star))
        if not video_urn:
            errors(lang('could_not_find_video_urn', item_star))

    else:
        errors(lang('could_not_find_toc_nd', item_star))
    return None

def getCourseSecsTocs(p,doc, course_slug,json_config):
    course_section_stars = p.find_all("contents")
    sections={}
    tocs={}
    for section_star in course_section_stars:
        section_star = section_star.text.strip()
        section_nd = doc.find('cachingKey',text=section_star)
        # print("213:%s" % section_star)
        if section_nd:
            section_nd_p = section_nd.parent
            section_title=section_nd_p.find("title")
            if section_title:
                section_title = section_title.text
                # print(section_title)
                section_slug=slugify(section_title)
                tocs[section_slug] = []
                sections[section_slug] = {
                    "title" : section_title
                }
                item_star_nds = section_nd_p.find_all("star_items")
                # item_stars=[]
                if item_star_nds:
                    for item_star_el in item_star_nds:
                        item_star = item_star_el.text
                        skip_pattern=r"urn:li:learningApiTocItem:urn:li:learningApiAssessmen"
                        match_skip_pattern=re.findall(skip_pattern,  item_star)
                        if len(match_skip_pattern)>0:
                            continue
                        # item_stars.append(item_star)
                        toc = getCourseToc(item_star,doc,course_slug,json_config)
                        if toc:
                            tocs[section_slug].append(toc)

    return [sections, tocs]  

def getCourseInfo(doc,json_config):
    rq_coure_nds=doc.find_all('request',text=lambda text: "/learning-api/courses" in text)
    for p in rq_coure_nds:
        rq_coure_nd = p

    match=None
    if rq_coure_nd:
        rq_coure_nd_p = rq_coure_nd.parent

        if rq_coure_nd_p:
            tbody =rq_coure_nd_p.find('tbody')
            # print(rq_coure_nd_p)

            if tbody:
                tbody = tbody.text
                pattern = r'\d+$'

                match = re.search(pattern, tbody)
    if not match:
        errors(lang('could_not_get_restli_request_body_content'))
        return None
    
    item_key='item_%s' % match.group()
    root_el = doc.find("%s" % item_key).find("value").find("data")
    # log(item_key)
    # print(root_el)

    if root_el:
        course_urn=root_el.find("star_elements")
        if not course_urn:
            course_urn=root_el.find("entityUrn")


        if course_urn:
            course_urn = course_urn.text
            entity_urn = doc.find('entityUrn',text=course_urn)
            # print(entity_urn)
            
            if entity_urn:
                p = entity_urn.parent
                course_slug = p.find('slug').text
                data={
                    "url" : "%s/%s" % (linkedin_learning_url, course_slug),
                    "slug" : course_slug,
                    "exerciseFiles" : None,
                    "sourceCodeRepository": None
                }
                title = p.find('title')
                if title:
                    data["title"] = title.text

                visibility = p.find('visibility')
                
                if visibility:
                    data["visibility"] = visibility.text

                viewerCounts = p.find('viewerCounts')
                if viewerCounts:
                    viewerCounts = viewerCounts.find('total')
                    if viewerCounts:
                        data["viewerCounts"] = int(viewerCounts.text)

                descriptionv2 = p.find('descriptionV2')
                
                if descriptionv2:
                    descriptionv2 = descriptionv2.find('text')
                    if descriptionv2:
                        data["descriptionv2"] = descriptionv2.text

                duration = p.find('duration')
                if duration:
                    duration = duration.find('duration')
                    if duration:
                        data["duration"] = int(duration.text)
                
                dificulty = p.find('dificulty')

                if dificulty:
                    dificulty = dificulty.find('difficultylevel')
                    if dificulty:
                        data["dificulty"] = dificulty.text


                descriptionv3 = p.find('descriptionV3')

                if descriptionv3:
                    descriptionv3 = descriptionv3.find('text')
                    if descriptionv3:
                        data["descriptionv3"] = descriptionv3.text


                sourceCodeRepo=p.find('sourceCodeRepository')
                if sourceCodeRepo:
                    data["sourceCodeRepository"]=sourceCodeRepo.text

                tags = ["sizeInBytes","name","url"]
                exerciseFiles = p.find('exerciseFiles')
                if exerciseFiles:
                    for tag in tags:
                        exercise_file_nd = exerciseFiles.find(tag) 
                        if exercise_file_nd:
                            exercise_file_nd = exercise_file_nd.text
                            if exercise_file_nd:
                                if not data["exerciseFiles"]:
                                    data["exerciseFiles"]={}
                                if tag == "sizeInBytes":     
                                    data["exerciseFiles"][tag]=int(exercise_file_nd)
                                else:
                                    data["exerciseFiles"][tag]=exercise_file_nd

                # data["primaryThumbnailV2"]=xmltodict.parse(str(p("primaryThumbnailV2")))
                # data["authors"]=xmltodict.parse(str(p("authors")))
                # data["authorsV2"]=xmltodict.parse(str(p("authorsv2")))
                # primarythumbnailv2
                # features > contentrating
                # urn star
                #   authors
                #   contents
                

                #  authorsv2
                # print(p("contents")) 
                sections, tocs = getCourseSecsTocs(p,doc, course_slug,json_config)   
                # data["sections"]=None
                data["sections"]=sections
                data["tocs"]=tocs
                # data["tocs"]=None
                # print(data)
                return data
    return None
def fetchCourseUrl(url,human=None,no_cache=True):
    course_url=cleanQueryString(url)
    prx=Prx(human)
    # print(course_url)
    content=prx.get(course_url, no_cache=no_cache)
    # print(content)
    if content:
        page_name=prx.getPageName()
        doc=pq(content)
        data=parseRestLiResponse(doc)
        # print(data)
        xml_doc=convert2Xml(data, page_name)
        return xml_doc
    else:
        errors(lang('could_not_fetch_course_url', course_url))
        errors(lang('are_you_connected_to_internet'))
    return None

def fetchCourseTocUrl(url,human=None):
    return fetchCourseUrl(url, human,no_cache=False)