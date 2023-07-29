from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base

class Toc(Base):
	__tablename__ = 'toc'

	id=Column(Integer,primary_key=True)
	sectionId=Column(String)
	title=Column(String)
	slug=Column(String)
	url=Column(String)
	duration=Column(String)
	captionUrl=Column(String)
	captionFmt=Column(String)
	streamLocationIds=Column(String)

	def __repr__(self):
		return f"<Toc(sectionId={self.sectionId},title={self.title},slug={self.slug},url={self.url},duration={self.duration},captionUrl={self.captionUrl},captionFmt={self.captionFmt},streamLocationIds={self.streamLocationIds},)>"
