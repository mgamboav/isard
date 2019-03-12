# Copyright 2017 the Isard-vdi project authors:
#      Josep Maria Viñolas Auquer
#      Alberto Larraz Dalmases
# License: AGPLv3

#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_login import login_required, current_user

from webapp import app

import rethinkdb as r
from ..lib.flask_rethink import RethinkDB
db = RethinkDB(app)
db.init_app(app)

from .decorators import ownsid

# ~ remote_addr=request.headers['X-Forwarded-For'].split(',')[0] if 'X-Forwarded-For' in request.headers else request.remote_addr.split(',')[0]

def valid_new_domain_dict(dict):
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
            
    # ~ ''' Data asked is allowed to the user '''
    # ~ if not dict['new_data']['kind'] in new_domain['new_data']['kind']:
        # ~ return False
        
    return True


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
@login_required
def get_desktops():
    try:
        data = app.isardlib.desktop_list(current_user)
        if data is False:
            abort(404)
        return jsonify(data)
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.error(exc_type, fname, exc_tb.tb_lineno)
        return json.dumps({'error': 'Unable to get desktop data from database'}), 500, {'ContentType':'application/json'}

@app.route('/api/desktops/<id>', methods = ['GET'])
@login_required
@ownsid
def get_desktops_id(id):
    try:
        data = app.isardlib.desktop_get(current_user,id)
        if data is False:
            abort(404)
        return jsonify(data)
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.error(exc_type, fname, exc_tb.tb_lineno)
        return json.dumps({'error': 'Unable to get desktop data from database'}), 500, {'ContentType':'application/json'}
        
@app.route('/api/desktops/<id>', methods = ['DELETE'])
@login_required
@ownsid
def delete_desktop(id):
    try:
        result = app.isardlib.desktop_delete(current_user,id)
        if result is False:
            abort(404)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.error(exc_type, fname, exc_tb.tb_lineno)
        return json.dumps({'error': 'Unable to get desktop data from database'}), 500, {'ContentType':'application/json'}

@app.route('/api/desktops', methods = ['POST'])    
@login_required
def add_desktop():
    try:
        if not request.json:
            abort(400)
        if not valid_new_domain_dict(request.json):
            abort(400)     
        if not app.isardlib.has_access(current_user,request.json['template']):
            abort(400)                                      
        if app.isardlib.desktop_add(current_user,request.json['template'],request.json['data']):
            return jsonify({})
        return json.dumps({'error': 'Unable to create desktop'}), 500, {'ContentType':'application/json'}
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.error(exc_type, fname, exc_tb.tb_lineno)
        return json.dumps({'error': 'Unable to get desktop data from database'}), 500, {'ContentType':'application/json'}


