import rethinkdb as r
from rethinkdb.errors import (
    ReqlAuthError,
    ReqlCursorEmpty,
    ReqlDriverError,
    ReqlError,
    ReqlInternalError,
    ReqlNonExistenceError,
    ReqlOpFailedError,
    ReqlOpIndeterminateError,
    ReqlPermissionError,
    ReqlQueryLogicError,
    ReqlResourceLimitError,
    ReqlRuntimeError,
    ReqlServerCompileError,
    ReqlTimeoutError,
    ReqlUserError)



class rdb():
    def __init__(self, RETHINK_HOST='localhost', RETHINK_PORT=28015, RETHINK_DB='isard'):
        self.conn = None
        self.rh=RETHINK_HOST
        self.rp=RETHINK_PORT
        self.rb=RETHINK_DB
    def __enter__(self):
        self.conn = r.connect(self.rh, self.rp, db=self.rb)
        return self.conn
    def __exit__(self, type, value, traceback):
        self.conn.close()
