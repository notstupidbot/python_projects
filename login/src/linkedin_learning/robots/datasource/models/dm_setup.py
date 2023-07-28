from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class DMSetup(Base):
	__tablename__ = 'dm_setup'

	id=Column(Integer,primary_key=True)
	courseId=Column(String)
	status=Column(String)
	finished=Column(String)
	availableFmt=Column(String)
	selectedFmt=Column(String)
	exerciseFile=Column(String)
	sourceRepo=Column(String)

	def __repr__(self):
		return f"<DMSetup(courseId={self.courseId},status={self.status},finished={self.finished},availableFmt={self.availableFmt},selectedFmt={self.selectedFmt},exerciseFile={self.exerciseFile},sourceRepo={self.sourceRepo},)>"
