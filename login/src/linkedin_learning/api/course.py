from robots import Human
from api.prx import Prx
import json
import re
import xmltodict
from robots.fn import errors, log, lang, cleanQueryString, pq, writeFile,slugify

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
    doc=pq(xml_content)
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

def getCourseInfo(doc):
    rq_coure_nd=doc('request:contains("/learning-api/courses")')
    match=None
    if rq_coure_nd:
        rq_coure_nd_p = rq_coure_nd.parent()
        if rq_coure_nd_p:
            tbody =rq_coure_nd_p('tbody')
            if tbody:
                tbody = tbody.text()
                pattern = r'\d+$'
                match = re.search(pattern, tbody)
    if not match:
        errors(lang('could_not_get_restli_request_body_content'))
        return None
    
    item_key='item_%s' % match.group()
    root_el = doc("%s > value > data" % item_key)

    if root_el:
        course_urn=root_el("star_elements")
        if course_urn:
            course_urn = course_urn.text()
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
                            "exerciseFiles" : None,
                            "sourceCodeRepository": None,
                            "duration" : int(p('duration>duration').text()),
                            "dificulty": p('difficultylevel').text(),
                            "viewerCounts" : int(p('viewercounts > total').text()),
                            "visibility" : p('visibility').text()
                        }
                        sourceCodeRepo=p('sourcecoderepository').text()
                        
                        if sourceCodeRepo:
                            data["sourceCodeRepository"]=sourceCodeRepo

                        tags = ["sizeInBytes","name","url"]
                        for tag in tags:
                            exercise_file_nd = p('exerciseFiles > %s' % tag) 
                            if exercise_file_nd:
                                exercise_file_nd = exercise_file_nd.text()
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
                        sections, tocs = getCourseSection(p,doc)   
                        data["sections"]=sections
                        data["tocs"]=tocs
                        # print(data)
                        return data
    return None


    # print(item_key)
def getTranscripts(v_meta_data_nd, doc):
    pg_transcript_nds = v_meta_data_nd("transcripts")
    transcripts=None
    tags = ["captionFormat","isAutogenerated","captionFile"] 
    # print(pg_transcript_nds)
    for pg_transcript_el in pg_transcript_nds:
        pg_transcript_nd = doc(pg_transcript_el)
        lang = pg_transcript_nd("locale > language").text()
        country = pg_transcript_nd("locale > country").text()
        if not transcripts:
            transcripts={}
            
        transcripts[lang] = {
            "country":country,
            "lang":lang
        }
        for tag in tags:
            transcripts[lang][tag] = pg_transcript_nd("%s" % tag).text()

    return transcripts
def getStreamLocations(v_meta_data_nd, doc):
    pg_stream_nds = v_meta_data_nd("progressiveStreams")
    stream_locations=None
    tags = ["size","bitRate","width","height"] 
    # print(pg_stream_nds)
    for pg_stream_el in pg_stream_nds:
        pg_stream_nd = doc(pg_stream_el)
        fmt = pg_stream_nd("height").text()
        if not stream_locations:
            stream_locations={}
            
        stream_locations[fmt] = {
            "url" : pg_stream_nd("streamingLocations > url").text(),
            "expiresAt" : int(pg_stream_nd("streamingLocations > expiresAt").text())
        }
        for tag in tags:
            stream_locations[fmt][tag] = int(pg_stream_nd("%s" % tag).text()) 

    return stream_locations
    # return None
def getVideoMeta(v_status_urn, doc):
    # urn:li:lyndaVideoViewingStatus:urn:li:lyndaVideo:(urn:li:lyndaCourse:2491193,3099399)
    # urn:li:lyndaVideoViewingStatus:urn:li:lyndaVideo:(urn:li:lyndaCourse:2491193,3094437)
    v_status_lookup = doc('star_lyndaVideoViewingStatus:contains("%s")' % v_status_urn)
    
    # print(v_status_lookup)
    stream_locations = None
    transcripts = None
    for el in v_status_lookup:
        el_nd = doc(el).parent()
        # parent_el = el_nd("parent")
        v_meta_data_nd = el_nd("presentation > videoPlay > videoPlayMetadata")
        if v_meta_data_nd:
            stream_locations = getStreamLocations(v_meta_data_nd, doc)
            transcripts = getTranscripts(v_meta_data_nd, doc)
        # v_meta_data_nd = el_nd("presentation > videoPlay")    
            # print(presentation_el)

    return [stream_locations,transcripts]
def getCourseToc(item_star, p,doc):
    toc_nd = doc('cachingKey:contains("%s")' % item_star).parent()
    if toc_nd:
        video_urn = toc_nd("content > video").text()
        if video_urn:
            # print(video_urn)
            entity_urn = doc('entityUrn:contains("%s")' % video_urn)
            if entity_urn:
                for entity in entity_urn:
                    entity_nd = doc(entity)
                    if entity_nd.text() == video_urn:
                        entity_nd_p = entity_nd.parent()
                        toc = {
                            "title" : entity_nd_p("title").text(),
                            "slug" : entity_nd_p("slug").text(),
                            "visibility" : entity_nd_p("visibility").text(),
                            "duration" : int(entity_nd_p("duration > duration").text()),
                            "v_status_urn" : entity_nd_p("star_lyndaVideoViewingStatus").text(),
                            "stream_locations" : None,
                            "transcripts" : None

                        }
                        stream_locations, transcripts = getVideoMeta(toc["v_status_urn"], doc)
                        if stream_locations:
                            toc["stream_locations"]=stream_locations
                        if transcripts:
                            toc["transcripts"]=transcripts
                        return toc

    return None

def getCourseSection(p,doc):
    course_section_stars = p("contents")
    sections={}
    tocs={}
    for section_star in course_section_stars:
        section_star = p(section_star).text()
        if section_star:
            section_nd = doc('cachingKey:contains("%s")' % section_star).parent()
            if section_nd:
                section_title=section_nd("title").text()
                section_slug=slugify(section_title)
                tocs[section_slug] = []
                sections[section_slug] = {
                    "title" : section_title
                }
                item_star_nds = section_nd("star_items")
                # item_stars=[]
                if item_star_nds:
                    for item_star_el in item_star_nds:
                        item_star = p(item_star_el).text()
                        # item_stars.append(item_star)
                        toc = getCourseToc(item_star,p,doc)
                        if toc:
                            tocs[section_slug].append(toc)

    return [sections, tocs]        

def fetchCourseUrl(url):
    course_url=cleanQueryString(url)
    prx=Prx()
    content=prx.get(course_url)
    page_name=prx.getPageName()
    doc=pq(content)
    data=parseRestLiResponse(doc)
    xml_doc=convert2Xml(data, page_name)
    return xml_doc