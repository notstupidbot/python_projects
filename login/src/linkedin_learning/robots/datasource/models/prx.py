from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base

class Prx(Base):
	__tablename__ = 'prx_cache'

	id=Column(Integer,primary_key=True)
	page_name=Column(String)
	content=Column(String)

	def __repr__(self):
		return f"<StreamLocation(page_name={self.page_name})>"

class MPrx:
	ds=None
	def __init__(self, ds):
		self.ds = ds
	
	def getByPageName(self, page_name):
		row = self.ds.session.query(Prx).filter_by(page_name=page_name).first()
		return row
	def deleteByPageName(self, page_name):
		row = self.ds.session.query(Prx).filter_by(page_name=page_name).first()
		if row:
			self.ds.session.delete(row)
			self.ds.session.commit()
	def create(self, page_name, content):
		existing = self.getByPageName(page_name)
		if existing:
			self.ds.session.delete(existing)

		rec = Prx(page_name=page_name, content=content)
		self.ds.session.add(rec)
		self.ds.session.commit()
		return rec
