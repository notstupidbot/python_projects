from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from robots.datasource.models import Config,User,App,Course,Section,Toc,StreamLocation,Transcript,DMSetup,DMStatus,AccountSetting 
from sqlalchemy.ext.declarative import declarative_base
from robots.datasource.models import MConfig
Base = declarative_base()

class DataSource:
    mConfig=None
    def __init__(self, path):
        # Replace 'sqlite:///your_database_name.db' with the actual path to your database file
        engine = create_engine('sqlite:///%s' % (path))
        Base.metadata.create_all(engine)
        User.metadata.create_all(engine)
        App.metadata.create_all(engine)
        Course.metadata.create_all(engine)
        Section.metadata.create_all(engine)
        Toc.metadata.create_all(engine)
        StreamLocation.metadata.create_all(engine)
        Transcript.metadata.create_all(engine)
        DMSetup.metadata.create_all(engine)
        DMStatus.metadata.create_all(engine)
        AccountSetting.metadata.create_all(engine)
        Config.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
        self.mConfig = MConfig(self.session)
