from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
import json
class Config(Base):
	__tablename__ = 'config'

	id=Column(Integer,primary_key=True)
	key=Column(String)
	value=Column(String)

	def __repr__(self):
		return f"<JSConfig(key={self.key},value={self.value})>"

class MConfig:
	def __init__(self, session):
		self.session = session
    
	def get(self,key,serialize=True):
		row = self.session.query(Config).filter_by(key=key).first()
		if row:
			if serialize:
				return json.loads(row.value)
		return row
   
	def set(self,key,value):
		config = self.get(key,serialize=False)
		value = json.dumps(value)
		if config:
			config.value = value
		else:
			config = Config()
			config.key=key
			config.value=value
			self.session.add(config)
		
		self.session.commit()
