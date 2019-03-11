# Copyright 2017 the Isard-vdi project authors:
#      Josep Maria Viñolas Auquer
#      Alberto Larraz Dalmases
# License: AGPLv3

#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_login import login_required, current_user
# ~ from flask_httpauth import HTTPBasicAuth

from webapp import app
from ...lib.admin_api import check as rc
from ...lib.api import get_all_alloweds_domains as get_allowed_templates

import rethinkdb as r
from .flask_rethink import RethinkDB
db = RethinkDB(app)
db.init_app(app)

from .decorators import ownsid

# ~ remote_addr=request.headers['X-Forwarded-For'].split(',')[0] if 'X-Forwarded-For' in request.headers else request.remote_addr.split(',')[0]

def parse_new_domain(dict,userDict){
    
    new_domain={'template':'',
                'new_data': {   'name': '',
                                'description': '',
                                'kind': ['template','base'],

                                'hardware': {   'vcpus': 0,
                                                'memory': 0,
                                                'graphics': '',
                                                'videos': '',
                                                'boot_order': [],
                                                'interfaces': [],
                                                'diskbus': '',
                                                'isos': [],
                                                'floppies': []}}}
    ''' It has all the keys '''
    if not new_domain.keys() == dict.keys():
        return False

    ''' User has access to this template to derivate '''
    with app.app_context():
        domains = get_allowed_templates(current_user.username, without=['history_domain','allowed'])
        domain = [d for d int domains if d['id'] == request.json['from_id']]
    if len(domain) == 0:
        return False
            
    ''' Data asked is allowed to the user '''
    if not dict['new_data']['kind'] in new_domain['new_data']['kind']:
        return False
    # Check 
        
    with app.app_context():
        # ~ userObj=r.table('users').get(user).pluck('id','category','group').run(db.conn)
        ephimeral_cat=r.table('categories').get(userObj['category']).pluck('ephimeral').run(db.conn)
        ephimeral_group=r.table('groups').get(userObj['group']).pluck('ephimeral').run(db.conn)
    ephimeral = ephimeral_group if 'ephimeral' in ephimeral_group.keys() else  ephimeral_cat
        
        # ~ dom=app.isardapi.get_domain(create_dict['template'])
            
        parent_disk=dom['hardware-disks'][0]['file']

        parsed_name = self.parse_string(create_dict['name'])
        dir_disk, disk_filename = self.get_disk_path(userObj, parsed_name)
        create_dict['hardware']['disks']=[{'file':dir_disk+'/'+disk_filename,
                                            'parent':parent_disk}]

        create_dict=self.parse_media_info(create_dict)
        
        new_domain={'id': '_'+user+'_'+parsed_name,
                  'name': create_dict['name'],
                  'description': create_dict['description'],
                  'kind': 'desktop',
                  'user': userObj['id'],
                  'status': 'Creating',
                  'detail': None,
                  'category': userObj['category'],
                  'group': userObj['group'],
                  'xml': None,
                  'icon': dom['icon'],
                  'server': dom['server'],
                  'os': dom['os'],
                  'options': {'viewers':{'spice':{'fullscreen':True}}},
                  'create_dict': {'hardware':create_dict['hardware'], 
                                    'origin': create_dict['template']}, 
                  'hypervisors_pools': create_dict['hypervisors_pools'],
                  'allowed': {'roles': False,
                              'categories': False,
                              'groups': False,
                              'users': False}}
        if 'ephimeral' in ephimeral.keys():
            new_domain['ephimeral']=ephimeral['ephimeral']


    return False


# ~ @auth.error_handler
# ~ def unauthorized():
    # ~ return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
    

@app.route('/api/desktops', methods = ['GET'])    
@app.route('/api/desktops/<id>', methods = ['GET'])
@login_required
@ownsid
def get_desktops(id=False):
    try:
        if id:
            with app.app_context():
                data = r.table('domains').get_all(current_user.user, index='user').filter({'id':id,'kind':'desktop'}).without('xml','history_domain').run(db.conn)
            if data is None:
                abort(404)
        else:
            with app.app_context():
                data = list(r.table('domains').get_all(current_user.user, index='user').filter('kind':'desktop').without('xml','history_domain').run(db.conn))
            if len(data) == 0:
                abort(404)
        return jsonify(data)
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.error(exc_type, fname, exc_tb.tb_lineno)
        return json.dumps({'error': 'Unable to get desktop data from database'}), 500, {'ContentType':'application/json'}

    # ~ return jsonify(list(r.table('domains').get_all(current_user.user, index='user').filter(r.row['kind'].match("template")).without('xml','history_domain').run(db.conn)))



@app.route('/api/desktops/<id>', methods = ['DELETE'])
@login_required
@ownsid
def delete_desktop(id):
    try:
        with app.app_context():
            domain = r.table('domains').get_all(current_user.user, index='user').filter({'id':id,'kind':'desktop'}).pluck('status').run(db.conn)
        if domain is None:
            abort(404)
        if domain['status'] not in ['Started']:
            with app.app_context():
                if rc(r.table('domains').get(id).update({'status':'Deleting'}).run(db.conn),'deleted'):
                    return jsonify({'result': True})
                else:
                    abort(404)
        else:
            return return json.dumps({'error':'Domain is not stopped. First stop the domain'}), 409, {'ContentType':'application/json'}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.error(exc_type, fname, exc_tb.tb_lineno)
        return json.dumps({'error': 'Unable to get desktop data from database'}), 500, {'ContentType':'application/json'}

@app.route('/api/desktops', methods = ['POST'])    
@login_required
@isAdmin
def add_desktop():
    try:
        if not request.json:
            abort(400)
        tem
        if not valid_new_domain_dict(request.json):
            abort(400)                                
        with app.app_context():
            domains = get_allowed_templates(current_user.username, without=['history_domain','allowed'])
            domain = [d for d int domains if d['id'] == request.json['from_id']]
        if len(domain) == 0:
            abort(404)

        default_keys = {'id':
                        'role':
                        'category':
                        'group':
                        'user':
                        'hypervisors_pools': ['default'],
                        'forced_hyp': 'default',
                        'accessed': time.time(),
                        'allowed': {'roles': False,
                                    'categories': False,
                                    'groups': False,
                                    'users': False}}
        
                 
        if status not in ['Started']:
            if rc(r.table('domains').get(id).update({'status':'Deleting'}).run(db.conn),'deleted'):
                return jsonify({'result': True})
            else:
                return json.dumps({}), 404, {'ContentType':'application/json'}
        else:
            return return json.dumps({'error':'Domain is not stopped. First stop the domain'}), 409, {'ContentType':'application/json'}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.error(exc_type, fname, exc_tb.tb_lineno)
        return json.dumps({'error': 'Unable to get desktop data from database'}), 500, {'ContentType':'application/json'}

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
@auth.login_required
def update_in_table(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify( { 'task': make_public_task(task[0]) } )
    

    
