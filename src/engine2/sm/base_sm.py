'''  BASES STATE MACHINE '''
    
class BaseSM():
    def __init__(self):
        self.states  = ['STOPPED','DELETED','FAILED']
        self.actions = ['DELETE','UPDATE','DESKTOP']
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
            self.transitions[init_state][action]['FAILED'] = False

    def define_machine(self):
        self.add_transition('STOPPED','DELETE','DELETED')
        self.add_transition('STOPPED','UPDATE','STOPPED')
        self.add_transition('STOPPED','DESKTOP','STOPPED')
        
        self.add_transition('FAILED','DELETE','DELETED')
        self.add_transition('FAILED','UPDATE','STOPPED')
        
    def get_states(self):
        return self.states
    
    def get_next_actions(self,state):
        if state == 'DELETED': return []
        if state in self.transitions.keys():
            return self.transitions[state].keys()
        raise StateInvalidError

class BaseSMError(Exception):
    pass
    
class StateInvalidError(BaseSMError):
    pass
