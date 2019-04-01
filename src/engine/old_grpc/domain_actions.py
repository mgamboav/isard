''' DOMAIN NEXT ACTIONS '''
import rethinkdb as r

try:
    from database import rdb
    # ~ from grpc_actions import GrpcActions
except:
    from engine.grpc.database import rdb
    # ~ from engine.grpc.grpc_actions import GrpcActions
    
class DomainActions():
    def __init__(self):
        desktop_actions = {  'STARTED':['START','DELETE','UPDATE','TEMPLATE'],
                    'STOPPED':['STOP','VIEWER'],
                    'FAILED' :['START','DELETE','UPDATE'}
    
    def for_desktop(self,desktop_id,state):
        state = state.capitalize()
        if state in self.actions.keys():
            try:
                with rdb() as conn:
                    r.table('domains').get(desktop_id).update({'next_actions':self.desktop_actions['state']}).run(conn)
                return self.desktop_actions['state']
            except:
                raise
        else:
            try:
                with rdb() as conn:
                    r.table('domains').get(desktop_id).update({'next_actions':[]}).run(conn)
                return []
            except:
                raise         

