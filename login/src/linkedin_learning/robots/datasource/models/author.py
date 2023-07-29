from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base

class Author(Base):
	__tablename__ = 'author'

	id=Column(Integer,primary_key=True)
	name=Column(String)
	slug=Column(String)
	biography=Column(String)
	shortBiography=Column(String)
	courseIds=Column(String)

	def __repr__(self):
		return f"<Author(name={self.name},slug={self.slug},biography={self.biography},shortBiography={self.shortBiography},courseIds={self.courseIds},)>"
