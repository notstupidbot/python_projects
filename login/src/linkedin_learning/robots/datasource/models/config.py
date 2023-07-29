from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base

import json
class Config(Base):
	__tablename__ = 'config'

	id=Column(Integer,primary_key=True)
	key=Column(String)
	value=Column(String)

	def __repr__(self):
		return f"<Config(key={self.key},value={self.value})>"

class MConfig:
	def __init__(self, session):
		self.session = session
    
	def get(self,key,serialize=True):
		row = self.session.query(Config).filter_by(key=key).first()
		if row:
			if serialize:
				return json.loads(row.value)
		return row
	
	def getData(self,keys=[]):
		data={}
		for key in keys:
			data[key] = self.get(key)
		return data
	def set(self,key,value):
		config = self.get(key,serialize=False)
		value = json.dumps(value)
		if config:
			config.value = value
		else:
			config = Config(key=key,value=value)
			self.session.add(config)
		
		self.session.commit()
