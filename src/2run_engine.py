from gevent.wsgi import WSGIServer

import time
from engine.services.log import logs

from flask import Flask
from logging.handlers import RotatingFileHandler


from engine.services.lib.functions import check_tables_populated
check_tables_populated()

from engine.services import db
from engine.models.manager_hypervisors import ManagerHypervisors

from engine.grpc.grpc_server import GrpcServer

class App(object):
    def __init():
        None


import asyncio



class App():
    def __init__(self, q):
        self._queue = q

    def _process_item(self, item):
        if item['process'] == 'parallel':
            print('The action '+item['action']+' should be run in parallel')
        else:
            print(f'The action '+item['action']+' should be run ordered')

    async def get_item(self):
        item = await self._queue.get()
        self._process_item(item)

    async def listen_for_orders(self):  
        '''
        Asynchronously check the orders queue for new incoming orders
        '''
        while True:
            # ~ asyncio.ensure_future(self.get_item())
            await self.get_item()

def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app.listen_for_orders())

if __name__ == "__main__":
    qq = asyncio.Queue()
    app = App(qq)
    app.loop = asyncio.get_event_loop()
    app.qq = qq

    import threading
    # ~ app.loop.run_until_complete(app.listen_for_orders())
    t = threading.Thread(target=loop_in_thread, args=(app.loop,), daemon=False)
    t.start()

    app.loop.call_soon_threadsafe(qq.put_nowait, {'process':'parallel','action':'start','domain':'_admin_tetros'})
    print('outof loop')
    ''' Manager Hypervisors '''
    app.m = ManagerHypervisors()
    print('ManagerHypervisors started...')

    ''' GRPC api '''
    app.grpc = GrpcServer(app)
    app.grpc.start_server()
    print('GRPC started...')
    app.loop.call_soon_threadsafe(qq.put_nowait, {'process':'ordered','action':'move_domain','domain':'_admin_tetros'})
    ''' Loop as nothing is blocking '''
    try:
        while True:
            time.sleep(60*60*60)
    except KeyboardInterrupt:
        app.grpc.stop_server()
        # ~ t.stop()
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
