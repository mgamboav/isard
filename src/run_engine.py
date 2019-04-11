# ~ from gevent.wsgi import WSGIServer

import time
from engine.services.log import logs

# ~ from flask import Flask
from logging.handlers import RotatingFileHandler


# ~ from engine.grpc.lib.database import populateDB
# ~ db = populateDB()
# ~ print(db.database())


# ~ from engine.services import db
from engine.models.manager_hypervisors import ManagerHypervisors

from engine.grpc.grpc_server import GrpcServer

class App(object):
    def __init():
        None

if __name__ == "__main__":
    app = App()
    ''' Manager Hypervisors '''
    app.m = ManagerHypervisors()
    print('ManagerHypervisors started...')

    ''' GRPC api '''
    app.grpc = GrpcServer(app)
    app.grpc.start_server()
    print('GRPC started...')
    
    ''' Loop as nothing is blocking '''
    try:
        while True:
            time.sleep(60*60*60)
    except KeyboardInterrupt:
        app.grpc.stop_server()

        app.m.stop_threads()
        while True:
            app.m.update_info_threads_engine()
            if len(app.m.threads_info_main['alive']) == 0 and len(app.m.threads_info_hyps['alive']) == 0:
                action = {}
                action['type'] = 'stop'
                app.m.q.background.put(action)
                break
            time.sleep(0.5)
        while True:
            if app.m.t_background.is_alive():
                time.sleep(0.2)
            else:
                delattr(app, 'm')
                break
        
        
        print('\nEngine stopped by keyboard interrupt ...\n')
