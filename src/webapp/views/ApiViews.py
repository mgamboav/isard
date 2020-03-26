# Copyright 2017 the Isard-vdi project authors:
#      Josep Maria Viñolas Auquer
#      Alberto Larraz Dalmases
# License: AGPLv3

#!flask/bin/python
# coding=utf-8
from flask import render_template, redirect, request, flash, url_for
from webapp import app
from flask_login import login_required, login_user, logout_user, current_user

from ..auth.authentication import *   
from ..lib.log import *    

from ..lib.isardViewer import isardViewer
isardviewer = isardViewer()                   

from uuid import uuid4
import time,json

class usrTokens():
    def __init__(self):
        self.tokens={}
        self.valid_seconds = 60 # Between client accesses to api

    def tkns(self):
        return self.tokens
        
    def add(self,usr):
        tkn=str(uuid4())[:32]
        self.tokens[tkn]={"usr":usr,"timestamp":time.time(),"domains":[]}
        return tkn
        # we should check other tokens for expiry time

    def valid(self,tkn):
        if tkn in self.tokens.keys():
            if time.time()-self.tokens[tkn]['timestamp']<self.valid_seconds:
                self.tokens[tkn]['timestamp']=time.time()
                return True
            else:
                self.tokens.pop(tkn,None)
        return False
        
####
    def autodesktop(self,usr,pwd,cat,gro):
        # CHECK IF USR ALREADY IN TOKENS??
        au=auth()
        if au.check(usr,pwd):
            return self.add(usr)
		
		
		if r.table('categories').get(cat).run() is None:
			self.result(r.table('categories').insert([{'id': cat,
													   'name': cat,
													   'description': cat,
													   'quota': r.table('roles').get('user').run()[
														   'quota']
													   }]).run())

		if r.table('groups').get(gro).run() is None:
			self.result(r.table('groups').insert([{'id': gro,
												   'name': gro,
												   'description': gro,
												   'quota': r.table('roles').get('user').run()['quota']
												   }]).run())

		if r.table('users').get(usr).run() is None:
			usr = [{'id': usr,
					'name': usr,
					'kind': 'local',
					'active': True,
					'accessed': time.time(),
					'username': usr,
					'password': pwd,
					'role': 'user',
					'category': cat,
					'group': gro,
					'mail': '',
					'quota': {'domains': {'desktops': 1,
										  'desktops_disk_max': 999999999,  # 1TB
										  'templates': 0,
										  'templates_disk_max': 999999999,
										  'running': 1,
										  'isos': 0,
										  'isos_disk_max': 999999999},
							  'hardware': {'vcpus': 2,
										   'memory': 3000000}},  # 10GB
					},
				   ]
			self.result(r.table('users').insert(usr, conflict='update').run())


        
        return False
####        
        
        
        
    # ~ def login(self,usr,pwd):
        # ~ # CHECK IF USR ALREADY IN TOKENS??
        # ~ au=auth()
        # ~ if au.check(usr,pwd):
            # ~ return self.add(usr)
        # ~ return False
    
    # ~ def domains(self,tkn):
        # ~ if not self.valid(tkn):
            # ~ return False
        # ~ usr_domains=app.isardapi.get_user_domains(self.tokens[tkn]['usr'])
        # ~ self.tokens[tkn]['domains']=[{'id':d['id'],'name':d['name'],'status':d['status']} for d in usr_domains]
        # ~ return self.tokens[tkn]['domains']

    def start(self,tkn,id):
        if not self.valid(tkn):
            return False
        if not any(d['id'] == id for d in self.tokens[tkn]['domains']):
            return False
        for d in self.tokens[tkn]['domains']:
            if d['id'] == id:
                if d['status'] in ['Stopped','Failed']:
                    app.isardapi.update_table_value('domains', id, 'status', 'Starting')
                    step=0
                    while step<5:
                        status=app.isardapi.get_domain(id)['status']
                        if status is not 'Starting':
                            return status
                        time.sleep(1)
                        step=step+1
                    return status
                elif d['status'] in ['Started']:
                    return d['status']
        return False

    def viewer(self,tkn,id,remote_addr):
        if not self.valid(tkn):
            return False   
        data={"pk":id,"kind":"file"}
        return isardviewer.get_viewer(data,self.tokens[tkn]['usr'],remote_addr)
        # SPICE {'kind':'file','ext':'vv','mime':'application/x-virt-viewer','content':'vv data file'}
        # PC VNC 'vnc','text/plain'
        
app.tokens=usrTokens() 

@app.route('/api/v1/autodesktop', methods=['POST'])
def api_v1_autodesktop():
	# Get data from middleware (already authenticated user)
    usr = request.get_json(force=True)['usr']
    pwd = request.get_json(force=True)['pwd']    ## Will be a token?
    cat = request.get_json(force=True)['categoy']
    gro = request.get_json(force=True)['group']
    
    # Validate or create user if not exists
    tkn=app.tokens.autodesktop(usr,pwd,cat,gro)

	# tkn will always be true as autodesktop doesn't check that
    if tkn is False:
		return json.dumps({"tkn":""}), 401, {'ContentType': 'application/json'}
	
	# Create new desktop based on usr category
	id = app.tokens.create_domain(tkn,usr,cat)
	if id is False:
		return json.dumps({"tkn":""}), 401, {'ContentType': 'application/json'}
	
	# Start new desktop and get viewer
	res=app.tokens.start(tkn,id)
	if res is False:
		return json.dumps({"code":0,"msg":"Token expired or not user domain"}), 403, {'ContentType': 'application/json'}
	if res == 'Failed':
		return json.dumps({"code":2,"msg":"Get domain message for failed..."}), 500, {'ContentType': 'application/json'}
	if res == 'Starting':
		return json.dumps({"code":1,"msg":"Engine seems to be down. Contact administrator."}), 500, {'ContentType': 'application/json'}
	if res == 'Started':
		# ~ remote_addr=request.headers['X-Forwarded-For'].split(',')[0] if 'X-Forwarded-For' in request.headers else request.remote_addr.split(',')[0]
        remote_addr='1.1.1.1'
		res=app.tokens.viewer(tkn,id,remote_addr)
		if res is False:
			return json.dumps({"code":0,"msg":"Token expired or not user domain"}), 403, {'ContentType': 'application/json'}
		else:
			return json.dumps(res), 200, {'ContentType': 'application/json'}

	return json.dumps({"code":1,"msg":"Unknown error. Domain status is: "+str(res)}), 500, {'ContentType': 'application/json'}
    
    

