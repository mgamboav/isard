''' DOMAIN NEXT ACTIONS '''
import rethinkdb as r

try:
    from database import rdb
    # ~ from grpc_actions import GrpcActions
except:
    from engine.grpc.database import rdb
    # ~ from engine.grpc.grpc_actions import GrpcActions

class MachineError(Exception):
    pass
    
class StateInvalidError(MachineError):
    pass
    
class DomainActions():
    def __init__(self):
        self.states  = ['STOPPED','STARTED','PAUSED','DELETED','FAILED','UNKNOWN']
        self.actions = ['STOP','START','PAUSE','RESUME','DELETE','UPDATE','TEMPLATE']
        self.transitions = {}
        
        self.define_machine()
        #~ import pprint
        #~ pprint.pprint(self.transitions)
                                
    def add_transition(self,init_state,action,end_state,expected=True):
        assert init_state in self.states
        assert action in self.actions
        assert end_state in self.states
        if init_state not in self.transitions.keys():
            self.transitions[init_state]={}
        if action not in self.transitions[init_state].keys():
            self.transitions[init_state][action] = {}
        self.transitions[init_state][action][end_state] = True
        self.transitions[init_state][action]['FAILED'] = False

    def define_machine(self):
        self.add_transition('STOPPED','START','STARTED')
        self.add_transition('STOPPED','DELETE','DELETED')
        self.add_transition('STOPPED','UPDATE','STOPPED')
        self.add_transition('STOPPED','TEMPLATE','STOPPED')
        
        self.add_transition('STARTED','STOP','STOPPED')
        self.add_transition('STARTED','PAUSE','PAUSED')
        
        self.add_transition('FAILED','START','STARTED')
        self.add_transition('FAILED','DELETE','DELETED')
        self.add_transition('FAILED','UPDATE','STOPPED')
        
        self.add_transition('PAUSED','RESUME','STARTED')
        self.add_transition('PAUSED','STOP','STOPPED')
        
        self.add_transition('UNKNOWN','DELETE','DELETED')
        
    def get_states(self):
        return [s.title() for s in self.states]
    
    def get_next_actions(self,state):
        if state in self.transitions.keys():
            return self.transitions[state].keys()
        raise StateInvalidError
        
    ''' UPDATING DATABASE. NOT USED '''            
    #~ def for_desktop(self,desktop_id,state):
        #~ state = state.capitalize()
        #~ if state in self.actions.keys():
            #~ try:
                #~ with rdb() as conn:
                    #~ r.table('domains').get(desktop_id).update({'next_actions':self.desktop_actions['state']}).run(conn)
                #~ return self.desktop_actions['state']
            #~ except:
                #~ raise
        #~ else:
            #~ try:
                #~ with rdb() as conn:
                    #~ r.table('domains').get(desktop_id).update({'next_actions':[]}).run(conn)
                #~ return []
            #~ except:
                #~ raise         

