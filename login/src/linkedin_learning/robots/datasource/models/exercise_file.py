from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base

class ExerciseFile(Base):
	__tablename__ = 'exercise_file'

	id=Column(Integer,primary_key=True)
	courseId=Column(String)
	name=Column(String)
	url=Column(String)
	size=Column(String)

	def __repr__(self):
		return f"<ExerciseFile(courseId={self.courseId},name={self.name},url={self.url},size={self.size},)>"

class MExerciseFile:
	ds=None
	def __init__(self, ds):
		self.ds = ds
    
	def getByCourseId(self,courseId):
		row = self.ds.session.query(ExerciseFile).filter_by(courseId=courseId).first()
		return row

	def create(self, name,url,size,courseId):
		existing = self.getByCourseId(courseId)
		if existing:
			return existing
		
		rec = ExerciseFile(name=name,url=url,size=size,courseId=courseId)
		self.ds.session.add(rec)
		self.ds.session.commit()
