from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from robots.datasource.models import User 
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class DataSource:
    def __init__(self, path):
        # Replace 'sqlite:///your_database_name.db' with the actual path to your database file
        engine = create_engine('sqlite:///%s' % (path))
        Base.metadata.create_all(engine)
        User.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()
        # try:
        #     new_user = User(name='John Doe', email='john@example.com')
        #     self.session.add(new_user)
        #     self.session.commit()
        # except Exception as e:
        #     print(e)
