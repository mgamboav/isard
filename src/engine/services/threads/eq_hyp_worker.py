# Copyright 2017 the Isard-vdi project authors:
#      Alberto Larraz Dalmases
#      Josep Maria Viñolas Auquer
# License: AGPLv3
# coding=utf-8


# ~ import queue
# ~ import threading
# ~ import time

# ~ from time import sleep

# ~ from libvirt import VIR_DOMAIN_START_PAUSED, libvirtError

# ~ from engine.models.hyp import hyp
# ~ from engine.services.db import get_hyp_hostname_from_id, update_db_hyp_info, update_domain_status, update_hyp_status, \
    # ~ update_domains_started_in_hyp_to_unknown, update_table_field, get_engine
# ~ from engine.services.lib.functions import get_tid, engine_restart
# ~ from engine.services.log import logs
# ~ from engine.services.threads.threads import TIMEOUT_QUEUES, launch_action_disk, RETRIES_HYP_IS_ALIVE, \
    # ~ TIMEOUT_BETWEEN_RETRIES_HYP_IS_ALIVE, launch_delete_media, launch_killall_curl
# ~ from engine.models.domain_xml import XML_SNIPPET_CDROM, XML_SNIPPET_DISK_VIRTIO, XML_SNIPPET_DISK_CUSTOM

# ~ class qeHypWorkerThread():
    # ~ def __init__(self, name, hyp_id, queue_actions, queue_master=None):
        # ~ threading.Thread.__init__(self)
        # ~ self.name = name
        # ~ self.hyp_id = hyp_id
        # ~ self.stop = False
        # ~ self.queue_actions = queue_actions
        # ~ self.queue_master = queue_master

from engine.services.db import get_hyp_hostname_from_id
from engine.models.hyp import hyp
from engine.services.log import logs
import time
from libvirt import libvirtError




def eq_hyp_worker(hyp_id, manager, action):
# ~ def eq_hyp_worker(hyp_id, action):
    # do={type:'start_domain','xml':'xml','id_domain'='prova'}
    print('manager')
    print('eq_hyp_worker: '+hyp_id)
    print('eq_hyp_worker: '+str(action['type']))
    # ~ action = self.queue_actions.get(timeout=TIMEOUT_QUEUES)

    # ~ logs.workers.debug('received action in working thread {}'.format(action['type']))

    if action['type'] == 'start_domain':
        logs.workers.debug('xml to start some lines...: {}'.format(action['xml'][30:100]))
        try:
            # ~ host, port, user = get_hyp_hostname_from_id(hyp_id)
            # ~ h = hyp(host, user=user, port=int(port))  
            # ~ time.sleep(10)
            h = manager.t_workers[hyp_id].h         
            h.conn.createXML(action['xml'])
            
            # wait to event started to save state in database
            #update_domain_status('Started', action['id_domain'], hyp_id=self.hyp_id, detail='Domain has started in worker thread')
            logs.workers.debug('STARTED domain {}: createdXML action in hypervisor {} has been sent'.format(
                action['id_domain'], host))
            return True
        except libvirtError as e:
            print(e)
            # ~ update_domain_status('Failed', action['id_domain'], hyp_id=self.hyp_id,
                                 # ~ detail=("Hypervisor can not create domain with libvirt exception: " + str(e)))
            logs.workers.debug('exception in starting domain {}: '.format(e))
            return False
        except Exception as e:
            print(e)
            # ~ update_domain_status('Failed', action['id_domain'], hyp_id=self.hyp_id, detail=("Exception when starting domain: " + str(e)))
            logs.workers.debug('exception in starting domain {}: '.format(e))
            return False

    ## STOP DOMAIN
    elif action['type'] == 'stop_domain':
        logs.workers.debug('action stop domain: {}'.format(action['id_domain'][30:100]))
        try:
            h = manager.t_workers[hyp_id].h         
            h.conn.lookupByName(action['id_domain']).destroy()

            logs.workers.debug('STOPPED domain {}'.format(action['id_domain']))
            return True
            # ~ check_if_delete = action.get('delete_after_stopped',False)

            # ~ if check_if_delete is True:
                # ~ update_domain_status('Stopped', action['id_domain'], hyp_id='')
                # ~ update_domain_status('Deleting', action['id_domain'], hyp_id='')
            # ~ else:
                # ~ update_domain_status('Stopped', action['id_domain'], hyp_id='')
            return False


        except Exception as e:
            # ~ update_domain_status('Failed', action['id_domain'], hyp_id=self.hyp_id, detail=str(e))
            logs.workers.debug('exception in stopping domain {}: '.format(e))
            return False

 
