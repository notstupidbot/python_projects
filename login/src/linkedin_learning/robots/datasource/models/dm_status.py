from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class DMStatus(Base):
	__tablename__ = 'dm_status'

	id=Column(Integer,primary_key=True)
	courseId=Column(String)
	vIndex=Column(String)
	metaStatus=Column(String)
	videoStatus=Column(String)
	captionStatus=Column(String)
	dtMetaStart=Column(String)
	dtVideoStart=Column(String)
	dtCaptionStart=Column(String)
	dtMetaEnd=Column(String)
	dtVideoEnd=Column(String)
	dtCaptionEnd=Column(String)
	dlMetaRetryCount=Column(String)
	dlCaptionRetryCount=Column(String)
	dlVideoRetryCount=Column(String)
	videoSz=Column(String)
	captionSz=Column(String)
	finished=Column(String)
	interupted=Column(String)

	def __repr__(self):
		return f"<DMStatus(courseId={self.courseId},vIndex={self.vIndex},metaStatus={self.metaStatus},videoStatus={self.videoStatus},captionStatus={self.captionStatus},dtMetaStart={self.dtMetaStart},dtVideoStart={self.dtVideoStart},dtCaptionStart={self.dtCaptionStart},dtMetaEnd={self.dtMetaEnd},dtVideoEnd={self.dtVideoEnd},dtCaptionEnd={self.dtCaptionEnd},dlMetaRetryCount={self.dlMetaRetryCount},dlCaptionRetryCount={self.dlCaptionRetryCount},dlVideoRetryCount={self.dlVideoRetryCount},videoSz={self.videoSz},captionSz={self.captionSz},finished={self.finished},interupted={self.interupted},)>"
