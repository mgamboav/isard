# ~ from sqlalchemy import create_engine
# ~ from sqlalchemy.orm import sessionmaker

# ~ engine = create_engine('postgresql://isardvdi:isardvdi@isard-database:5432/engine')

# ~ Session = sessionmaker(bind=engine)

# ~ class SessionManager(object):
    # ~ def __init__(self):
        # ~ self.session = Session()


from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import DB_URL
# ~ DB_CONNECTION='sqlite:///:memory:'
engine = create_engine(DB_URL, convert_unicode=True)
# ~ engine = create_engine('sqlite:///:memory:')



# ~ session = scoped_session(sessionmaker(bind=engine))

# ~ @contextmanager
# ~ def db_session():
    # ~ """ Creates a context with an open SQLAlchemy session.
    # ~ """
    # ~ engine = create_engine('postgresql://isardvdi:isardvdi@isard-database:5432/engine', convert_unicode=True)
    # ~ connection = engine.connect()
    # ~ db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    # ~ yield db_session
    # ~ db_session.close()
    # ~ connection.close()

# ~ @contextmanager
# ~ def db_engine():
    # ~ engine = create_engine('postgresql://isardvdi:isardvdi@isard-database:5432/engine', convert_unicode=True).connect()
    # ~ yield engine
    # ~ engine.close()
