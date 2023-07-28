from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class StreamLocation(Base):
	__tablename__ = 'stream_location'

	id=Column(Integer,primary_key=True)
	tocId=Column(String)
	fmt=Column(String)
	url=Column(String)
	expiresAt=Column(String)

	def __repr__(self):
		return f"<StreamLocation(tocId={self.tocId},fmt={self.fmt},url={self.url},expiresAt={self.expiresAt})>"
