from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Section(Base):
	__tablename__ = 'section'

	id=Column(Integer,primary_key=True)
	courseId=Column(String)
	slug=Column(String)
	title=Column(String)
	tocIds=Column(String)

	def __repr__(self):
		return f"<Section(courseId={self.courseId},slug={self.slug},title={self.title},tocIds={self.tocIds},)>"
