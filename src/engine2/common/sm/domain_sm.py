''' DOMAINS STATE MACHINE '''
    
class DomainSM():
    def __init__(self):
        self.states  = ['STATE_STOPPED','STATE_STARTED','STATE_PAUSED','STATE_DELETED','STATE_FAILED','STATE_UNKNOWN']
        self.actions = ['ACTION_STOP','ACTION_START','ACTION_PAUSE','ACTION_RESUME','ACTION_DELETE','ACTION_UPDATE','ACTION_TEMPLATE']
        self.transitions = {}
        
        self.define_machine()
                                
    def add_transition(self,init_state,action,end_state,expected=True):
        assert init_state in self.states
        assert action in self.actions
        assert end_state in self.states
        if init_state not in self.transitions.keys():
            self.transitions[init_state]={}
        if action not in self.transitions[init_state].keys():
            self.transitions[init_state][action] = {}
            self.transitions[init_state][action][end_state] = True
            self.transitions[init_state][action]['STATE_FAILED'] = False

    def define_machine(self):
        self.add_transition('STATE_STOPPED','ACTION_START','STATE_STARTED')
        self.add_transition('STATE_STOPPED','ACTION_DELETE','STATE_DELETED')
        self.add_transition('STATE_STOPPED','ACTION_UPDATE','STATE_STOPPED')
        self.add_transition('STATE_STOPPED','ACTION_TEMPLATE','STATE_STOPPED')
        
        self.add_transition('STATE_STARTED','ACTION_STOP','STATE_STOPPED')
        self.add_transition('STATE_STARTED','ACTION_PAUSE','STATE_PAUSED')
        
        self.add_transition('STATE_FAILED','ACTION_START','STATE_STARTED')
        self.add_transition('STATE_FAILED','ACTION_DELETE','STATE_DELETED')
        self.add_transition('STATE_FAILED','ACTION_UPDATE','STATE_STOPPED')
        
        self.add_transition('STATE_PAUSED','ACTION_RESUME','STATE_STARTED')
        self.add_transition('STATE_PAUSED','ACTION_STOP','STATE_STOPPED')
        
        self.add_transition('STATE_UNKNOWN','ACTION_DELETE','STATE_DELETED')
        
    def get_states(self):
        return self.states
    
    def get_next_actions(self,state):
        if state == 'STATE_DELETED': return []
        if state in self.transitions.keys():
            return list(self.transitions[state].keys())
        raise StateInvalidError

class DomainSMError(Exception):
    pass
    
class StateInvalidError(DomainSMError):
    # raise InvalidArgument
    pass
