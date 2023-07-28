from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Course(Base):
	__tablename__ = 'course'

	id=Column(Integer,primary_key=True)
	title=Column(String)
	slug=Column(String)
	duration=Column(String)
	sourceCodeRepository=Column(String)
	description=Column(String)
	authorIds=Column(String)
	urn=Column(String)

	def __repr__(self):
		return f"<Course(title={self.title},slug={self.slug},duration={self.duration},sourceCodeRepository={self.sourceCodeRepository},description={self.description},authorIds={self.authorIds},urn={self.urn},)>"
