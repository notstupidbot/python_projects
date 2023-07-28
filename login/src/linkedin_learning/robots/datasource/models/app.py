from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class App(Base):
	__tablename__ = 'app'

	id=Column(Integer,primary_key=True)
	version=Column(String)
	state=Column(String)
	lastCourseSlug=Column(String)
	nav=Column(String)
	freshInstall=Column(String)

	def __repr__(self):
		return f"<App(version={self.version},state={self.state},lastCourseSlug={self.lastCourseSlug},nav={self.nav},freshInstall={self.freshInstall},)>"
