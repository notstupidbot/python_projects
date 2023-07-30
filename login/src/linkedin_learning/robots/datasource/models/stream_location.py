from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base

class StreamLocation(Base):
	__tablename__ = 'stream_location'

	id=Column(Integer,primary_key=True)
	tocId=Column(String)
	fmt=Column(String)
	url=Column(String)
	expiresAt=Column(String)

	def __repr__(self):
		return f"<StreamLocation(tocId={self.tocId},fmt={self.fmt},url={self.url},expiresAt={self.expiresAt})>"

class MToc:
	ds=None
	def __init__(self, ds):
		self.ds = ds
	
	def getByFmt(self, fmt, tocId):
		q = self.ds.session.query(StreamLocation).filter_by(fmt=fmt, tocId=tocId)

		return q.first()

	def create(self, tocId, fmt, url, expiresAt):
		existing = self.getByFmt(fmt, tocId)
		if existing:
			return existing
		
		rec = StreamLocation(tocId=tocId, fmt=fmt, url=url, expiresAt=expiresAt)
		self.ds.session.add(rec)
		self.ds.session.commit()
		return rec
