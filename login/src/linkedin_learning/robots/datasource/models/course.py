from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base, author_course_association
from sqlalchemy.orm import relationship

class Course(Base):
	__tablename__ = 'course'

	id=Column(Integer,primary_key=True)
	title=Column(String)
	slug=Column(String)
	duration=Column(String)
	sourceCodeRepository=Column(String)
	description=Column(String)
	urn=Column(String)
	authors = relationship('Author', secondary=author_course_association, back_populates='courses')


	def __repr__(self):
		return f"<Course(title={self.title},slug={self.slug},duration={self.duration},sourceCodeRepository={self.sourceCodeRepository},description={self.description},urn={self.urn})>"

class MCourse:
	ds=None
	def __init__(self, ds):
		self.ds = ds
    
	def get(self,id):
		row = self.ds.session.query(Course).filter_by(id=id).first()
		return row
	
	def getBySlug(self,slug):
		row = self.ds.session.query(Course).filter_by(slug=slug).first()
		return row
	def getList(self):
		rows = self.ds.session.query(Course).all()
		return rows
	def addAuthor(self,course, author):
		course.authors.append(author)
		self.ds.session.commit()
	def getLastSlug(self,keys=[]):
		pass
	
	def setLastSlug(self):
		pass
	
	def addAuthorId(self):
		pass
	
	def getCoursePageData(self):
		pass
	
	def getCourseSecsTocs(self):
		pass
	
	def create(self, title, slug, duration, sourceCodeRepository, description, urn):
		existing = self.getBySlug(slug)
		if existing:
			return existing
		course = Course(title=title, slug=slug, duration=duration, sourceCodeRepository=sourceCodeRepository, description=description, urn=urn)
		self.ds.session.add(course)
		self.ds.session.commit()
		
		return course
	
	def update(self,id,row):
		pass