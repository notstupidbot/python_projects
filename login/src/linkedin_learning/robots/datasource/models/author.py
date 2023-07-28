from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Author(Base):
	__tablename__ = 'app'

	id=Column(Integer,primary_key=True)
	name=Column(String)
	slug=Column(String)
	biography=Column(String)
	shortBiography=Column(String)
	courseIds=Column(String)

	def __repr__(self):
		return f"<App(name={self.name},slug={self.slug},biography={self.biography},shortBiography={self.shortBiography},courseIds={self.courseIds},)>"
