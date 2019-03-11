# Copyright 2017 the Isard-vdi project authors:
#      Josep Maria Viñolas Auquer
#      Alberto Larraz Dalmases
# License: AGPLv3

#!/usr/bin/env python
# coding=utf-8
import random, queue
from threading import Thread
import time, json, sys
from webapp import app
from flask_login import current_user
import rethinkdb as r
from ..lib.log import * 

from .flask_rethink import RethinkDB
db = RethinkDB(app)
db.init_app(app)

from .admin_api import flatten
from ..auth.authentication import Password  

from netaddr import IPNetwork, IPAddress 

class isard_lib():
    def __init__(self):
        pass

    ''' HELPERS '''
    def _rdbcheck(self,dict,action):
        '''
        These are the actions:
        {u'skipped': 0, u'deleted': 1, u'unchanged': 0, u'errors': 0, u'replaced': 0, u'inserted': 0}
        '''
        if dict[action]: 
            return True
        if not dict['errors']: return True
        return False

    def _parse_string(self, txt):
        import re, unicodedata, locale
        if type(txt) is not str:
            txt = txt.decode('utf-8')
        #locale.setlocale(locale.LC_ALL, 'ca_ES')
        prog = re.compile("[-_àèìòùáéíóúñçÀÈÌÒÙÁÉÍÓÚÑÇ .a-zA-Z0-9]+$")
        if not prog.match(txt):
            return False
        else:
            # ~ Replace accents
            txt = ''.join((c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn'))
            return txt.replace(" ", "_")

    def _get_disk_path(self, userObj, parsed_name):
        dir_path = userObj['category']+'/'+userObj['group']+'/'+userObj['id']
        filename = parsed_name + '.qcow2'
        return dir_path,filename
        
    def _quota_check(self,user,kind,action):
        if kind == 'desktop':
            if action == 'add':
                if user['quota']['domains']['desktops'] >= len(self.desktop_list(user)):
                    return False
            if action == 'start':
                with app.app_context():
                    user_started_desktops = r.table('domains').get_all(user.id, index='user').filter({'kind': 'desktop','status':'Started'}).count().run(db.conn)
                if user['quota']['domains']['running'] >= user_started_desktops:
                    return False  
            return True
        if kind == 'media':
            if action == 'add':
                if user['quota']['domains']['isos'] >= len(self.media_list(user)):
                    return False  
            return True
        if kind == 'template':
            if action == 'add':
                if user['quota']['domains']['isos'] >= len(self.template_list(user):
                    return False  
            return True
            
    ''' DESKTOPS '''
    def desktop_get(self,user,id):
        with app.app_context():
            data = list(r.table('domains').get_all(current_user.user, index='user').filter({'id':id,'kind':'desktop'}).without('xml','history_domain').run(db.conn))
        if len(data) == 0:
            return False
        return data[0]
        
    def desktop_list(self,user):
        with app.app_context():
            data = list(r.table('domains').get_all(current_user.user, index='user').filter('kind':'desktop').without('xml','history_domain').run(db.conn))
        if len(data) == 0:
            return False
        return data
                
    def desktop_add(self,user,from_template_id,data):
        if not self._quota_check(user,'desktop','add'):
            return False

        ''' Parsed name to be used in id and disk name '''
        name_parsed = self._parse_string(data['name'])            
        new_id = '_'+user.id+'_'+name_parsed
        
        ''' Checking if domain exists: '''
        if r.table('domains').get(new_id).run(db.conn) is not None: return False
        
        ''' Allowed template?? '''
        template = self.template_get(user,from_template_id)
        if template is False:
            return False
        
        ''' Hard disk path and name '''
        dir_disk, disk_filename = self.get_disk_path(user, name_parsed)

        ''' Media list '''
        medias=['isos','floppies','storage']
        for m in medias:
            if m in data['hardware']:
                newlist=[]
                for item in data['hardware'][m]:
                    with app.app_context():
                        newlist.append(r.table('media').get(item['id']).pluck('id','name','description').run(db.conn))
                template['hardware'][m]=newlist
        
        ''' Domain definition '''
        new_domain={  'id':             new_id,
                      'name':           data['name'],
                      'description':    data['description'],
                      'kind':           'desktop',
                      'user':           user.id,
                      'status':         'Creating',
                      'detail':         None,
                      'category':       user.category,
                      'group':          user.group,
                      'xml':            None,
                      'icon':           template['icon'],
                      'server':         template['server'],
                      'os':             template['os'],
                      'options':        {   'viewers':{'spice':{'fullscreen': True }}},
                      'create_dict':    {   'hardware':template['hardware'], 
                                            'origin': from_template_id}, 
                      'hypervisors_pools': template['hypervisors_pools'],
                      'hardware':       {'disks':[{ 'file':dir_disk+'/'+disk_filename,
                                                    'parent':template['hardware-disks'][0]['file']}]}}
                      'allowed':        {'roles': False,
                                            'categories': False,
                                            'groups': False,
                                            'users': False}}
        ''' Ephimeral desktops (timed) '''
        with app.app_context():
            ephimeral_cat=r.table('categories').get(user.category).pluck('ephimeral').run(db.conn)
            ephimeral_group=r.table('groups').get(user.group).pluck('ephimeral').run(db.conn)
        ephimeral = ephimeral_group if 'ephimeral' in ephimeral_group.keys() else  ephimeral_cat                                            
        if 'ephimeral' in ephimeral.keys():
            new_domain['ephimeral']=ephimeral['ephimeral']        
        
        ''' Insert new domain '''
        with app.app_context():
            return self._rdbcheck(r.table('domains').insert(new_domain).run(db.conn),'inserted')
        
    def desktop_update(self,user,data):
        None
        
    def desktop_delete(self,user,id):
        with app.app_context():
            domain = list(r.table('domains').get_all(user.id, index='user').filter({'id':id,'kind':'desktop'}).pluck('status').run(db.conn))
        if len(domain) == 0:
            return False
        if domain['status'] not in ['Started','Starting']:
            with app.app_context():
                if self._rdbcheck(r.table('domains').get(id).update({'status':'Deleting'}).run(db.conn),'deleted'):
                    return True
        return False
                
    def desktop_start(self,user,id):
        if not self._quota_check(user,'desktop','start')
        with app.app_context():
            domain = list(r.table('domains').get_all(user.id, index='user').filter({'id':id,'kind':'desktop'}).pluck('status').run(db.conn))
        if len(domain) == 0:
            return False
        if domain['status'] not in ['Started','Starting']:
            with app.app_context():
                if self._rdbcheck(r.table('domains').get(id).update({'status':'Starting'}).run(db.conn),'updated'):
                    return True
        return False
        
    def desktop_stop(self,user,id):
        with app.app_context():
            domain = list(r.table('domains').get_all(user.id, index='user').filter({'id':id,'kind':'desktop'}).pluck('status').run(db.conn))
        if len(domain) == 0:
            return False
        if domain['status'] in ['Started']:
            with app.app_context():
                if self._rdbcheck(r.table('domains').get(id).update({'status':'Stopping'}).run(db.conn),'updated'):
                    return True
        return False    

    ''' TEMPLATES '''
    def template_get(self,user,id):
        with app.app_context():
            data_tmpl = list(r.table('domains').get_all(user.id, index='user').filter(r.row['kind'].match("template")).filter({'id':id}).without('xml','history_domain').run(db.conn))
            data_base = list(r.table('domains').get_all(user.id, index='user').filter({'id':id,'kind':'base'}).without('xml','history_domain').run(db.conn))
            data = data_tmpl + data_base
        if len(data) == 0:
            return False
        return data[0]
                
    def template_list(self,user):
        with app.app_context():
            data_tmpl = list(r.table('domains').get_all(user.id, index='user').filter(r.row['kind'].match("template")).without('xml','history_domain').run(db.conn))
            data_base = list(r.table('domains').get_all(current_user.user, index='user').filter('kind':'base').without('xml','history_domain').run(db.conn))
            data = data_tmpl + data_base
        if len(data) == 0:
            return False
        return data
                    
    def template_add(self,user,from_desktop_id,data):
        if not self._quota_check(user,'template','add'):
            return False        

        with app.app_context():
            template=r.table('domains').get(from_desktop_id).run(db.conn)
        name_parsed = self.parse_string(name['name'])
        data['id'] = '_' + user.id + '_' + name_parsed
        ''' Checking if domain exists: '''
        if r.table('domains').get(data['id']).run(db.conn) is not None: return False
        
        data['create_dict']['hardware']['disks']=template['create_dict']['hardware']['disks']
        
        template['create_dict']['template_dict']={**template,**data}
        template['create_dict']['origin']=from_desktop_id
        
        dir_disk, disk_filename = self.get_disk_path(u, name_parsed)
        template['create_dict']['hardware']['disks'][0]={'file':dir_disk+'/'+disk_filename, 'parent':''}  #, 'bus':part_dict['create_dict']['hardware']['diskbus']}  
        data['create_dict']['hardware'].pop('diskbus',None)
                
        with app.app_context():
            return self.check(r.table('domains').get(from_desktop_id).update({"create_dict": template['create_dict'], "status": "CreatingTemplate"}).run(db.conn),'replaced')
                        
    def template_update(self,user,data):
        None
        
    def template_delete(self,user,id):
        ''' Warning! Domains could not be owned by the user! '''
        
        '''This is the only needed if it works StoppingAndDeleting'''
        # ~ r.table('domains').get_all(r.args(newids)).update({'status':'StoppingAndDeleting'}).run(db.conn) 
        
        domains = self.template_childs(user,id)

        started=[d['id'] for d in domains if d['status'] == 'Started']
        res=r.table('domains').get_all(r.args(started)).update({'status':'Stopping'}).run(db.conn)
        if res['replaced'] > 0:
            ''' Wait a bit for domains to be stopped... '''
            for i in range(0,10):
                time.sleep(.5)
                if r.table('domains').get_all(r.args(started)).filter({'status':'Stopping'}).pluck('status').run(db.conn) is None:
                    r.table('domains').get_all(r.args(started)).filter({'status':'Stopped'}).update({'status':'Maintenance'}).run(db.conn) 
                    break
                else:
                    r.table('domains').get_all(r.args(started)).filter({'status':'Stopped'}).update({'status':'Maintenance'}).run(db.conn) 
        r.table('domains').get_all(r.args(started)).update({'status':'Stopped'}).run(db.conn) 
        r.table('domains').get_all(r.args(started)).update({'status':'Deleting'}).run(db.conn) 
        return True
        
    def template_childs(self,user,id):
        with app.app_context():
            domain_id=r.table('domains').get(id).pluck('id','name','kind','user','status','parents').run(db.conn)
            domains = list(r.table('domains').pluck('id','name','kind','user','status','parents').filter(lambda derivates: derivates['parents'].contains(id)).run(db.conn))
        return [domain_id]+domains
            
    ''' MEDIA '''
    def media_get(self,user,id):
        with app.app_context():
            data = list(r.table('media').get_all(current_user.user, index='user').filter({'id':id}).run(db.conn))
        if len(data) == 0:
            return False
        return data[0]
                
    def media_list(self,user):
        with app.app_context():
            data = list(r.table('media').get_all(current_user.user, index='user').run(db.conn))
        if len(data) == 0:
            return False
        return data   
             
    def media_add(self,user,data):
        if not self._quota_check(user,'desktop','add'):
            return False
                    
    def media_update(self,user,data):
        None
        
    def media_delete(self,user,id):
        ''' Needs optimization by directly doing operation in nested array of dicts in reql '''
        domains=self.media_domains_plugged(user,id)
        # ~ domids=[d['id'] for d in domains]
        for dom in domains:
            domain_id=dom['id']
            ''' We could unplug from started domains, but no update should be done... '''
            if dom['status'] == 'Started': continue
            if dom['status'] != 'Stopped':
                r.table('domains').get(domain_id).update({'status':'Stopped'}).run(db.conn)
            dom['create_dict']['hardware']['isos'][:]= [iso for iso in dom['create_dict']['hardware']['isos'] if iso.get('id') != id]
            dom.pop('id',None)
            dom.pop('name',None)
            dom.pop('kind',None)
            dom['status']='Updating'
            with app.app_context():
                r.table('domains').get(domain_id).update(dom).run(db.conn)
        return True

    def media_domains_plugged(self,user,id):
        with app.app_context():
            return list(r.table('domains').filter( lambda dom: dom['create_dict']['hardware']['isos'].contains( lambda media: media['id'].eq(id))).pluck('id','name','kind','status', { "create_dict": { "hardware": {"isos"}}}).run(db.conn))

        
    ''' USER '''
    def user_get(self,user,id):
        if user.id != id: return False
        with app.app_context():
            data = list(r.table('users').get(id).without('password').run(db.conn))
        if len(data) == 0:
            return False
        return data[0]
        
    def user_update(self,user,id):
        None
        
    def user_delete(self,user,id):
        None
        
    def update_user_password(self,user,id,passwd):
        if user.id != id: return False
        pw=Password()
        with app.app_context():
            return self._rdbcheck(r.table('users').get(id).update({'password':pw.encrypt(passwd)).run(db.conn),'replaced')        
    






    ''' ACCESSIBLE FOR USER '''
    def get_allowed_system_templates(self,user):
        with app.app_context():
            ud=r.table('users').get(user.id).run(db.conn)
            data1 = r.table('domains').get_all('base', index='kind').order_by('name').pluck({'id','name','allowed','kind','group','icon','user','description'}).run(db.conn)
            data2 = r.table('domains').filter(r.row['kind'].match("template")).order_by('name').pluck({'id','name','allowed','kind','group','icon','user','description'}).run(db.conn)
        data = data1+data2
        alloweds=[]
        for d in data:
            with app.app_context():
                d['username']=r.table('users').get(d['user']).pluck('name').run(db.conn)['name']
            if ud['role']=='admin': 
                alloweds.append(d)
                continue
            if d['user']==ud['id']:
                alloweds.append(d)
                continue
            if d['allowed']['roles'] is not False:
                if len(d['allowed']['roles'])==0:
                    alloweds.append(d)
                    continue
                else:
                    if ud['role'] in d['allowed']['roles']:
                        alloweds.append(d)
                        continue
            if d['allowed']['categories'] is not False:
                if len(d['allowed']['categories'])==0:
                    alloweds.append(d)
                    continue
                else:
                    if ud['category'] in d['allowed']['categories']:
                        alloweds.append(d)
                        continue
            if d['allowed']['groups'] is not False:
                if len(d['allowed']['groups'])==0:
                    alloweds.append(d)
                    continue
                else:
                    if ud['group'] in d['allowed']['groups']:
                        alloweds.append(d)
                        continue
            if d['allowed']['users'] is not False:
                if len(d['allowed']['users'])==0:
                    alloweds.append(d)
                    continue
                else:
                    if ud['id'] in d['allowed']['users']:
                        alloweds.append(d)
                        continue 
        return alloweds
    
    def get_quotas(self,user):
        with app.app_context():
            if not fakequota==False: user_obj['quota']=fakequota
            desktops=len(self.desktop_list(user))
            desktopsup=r.table('domains').get_all(user.id, index='user').filter({'kind': 'desktop','status':'Started'}).count().run(db.conn)
            templates=len(self.template_list(user))
            isos=len(self.media_list(user))
            try:
                qpdesktops=desktops*100/user_obj['quota']['domains']['desktops']
            except Exception as e:
                qpdesktops=100
            try:
                qpup=desktopsup*100/user_obj['quota']['domains']['running']
            except Exception as e:
                qpup=100
            try:
                qptemplates=templates*100/user_obj['quota']['domains']['templates']
            except:
                qptemplates=100
            try:
                qpisos=isos*100/user_obj['quota']['domains']['isos']
            except:
                qpisos=100
        #~ return {'d':desktops,  'dq':user_obj['quota']['domains']['desktops'],  'dqp':"%.2f" % 0,
                #~ 'r':desktopsup,'rq':user_obj['quota']['domains']['running'],   'rqp':"%.2f" % 0,
                #~ 't':templates, 'tq':user_obj['quota']['domains']['templates'], 'tqp':"%.2f" % 0,
                #~ 'i':isos,      'iq':user_obj['quota']['domains']['isos'],      'iqp':"%.2f" % 0}
        return {'d':desktops,  'dq':user_obj['quota']['domains']['desktops'],  'dqp':"%.2f" % round(qpdesktops,2),
                'r':desktopsup,'rq':user_obj['quota']['domains']['running'],   'rqp':"%.2f" % round(qpup,2),
                't':templates, 'tq':user_obj['quota']['domains']['templates'], 'tqp':"%.2f" % round(qptemplates,2),
                'i':isos,      'iq':user_obj['quota']['domains']['isos'],      'iqp':"%.2f" % round(qpisos,2)}
        
    def get_allowed_tables(self,user,table=False):
