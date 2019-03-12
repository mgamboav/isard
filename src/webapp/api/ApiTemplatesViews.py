# Copyright 2017 the Isard-vdi project authors:
#      Josep Maria Viñolas Auquer
#      Alberto Larraz Dalmases
# License: AGPLv3

#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_login import login_required, current_user
# ~ from flask_httpauth import HTTPBasicAuth

from webapp import app
# ~ from ...lib.admin_api import check as rc
# ~ from ...lib.api import get_all_alloweds_domains as get_allowed_templates

import rethinkdb as r
from ..lib.flask_rethink import RethinkDB
db = RethinkDB(app)
db.init_app(app)

from .decorators import ownsid

import sys,os, json
from ..lib.log import * 

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
    

@app.route('/api/templates', methods = ['GET'])    
@app.route('/api/templates/<id>', methods = ['GET'])
@login_required
@ownsid
def get_templates(id=False):
    try:
        if id:
            data = app.isardlib.template_get(current_user,id)
            if data is False:
                abort(404)
        else:
            data = app.isardlib.template_list(current_user)
            if data is False:
                abort(404)
        return jsonify(data)
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.error(exc_type, fname, exc_tb.tb_lineno)
        return json.dumps({'error': 'Unable to get desktop data from database'}), 500, {'ContentType':'application/json'}

    # ~ return jsonify(list(r.table('domains').get_all(current_user.user, index='user').filter(r.row['kind'].match("template")).without('xml','history_domain').run(db.conn)))



@app.route('/api/templates/<id>', methods = ['DELETE'])
@login_required
@ownsid
def delete_template(id):
    try:
        result = app.isardlib.template_delete(current_user,id)
        if result is False:
            abort(404)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.error(exc_type, fname, exc_tb.tb_lineno)
        return json.dumps({'error': 'Unable to get desktop data from database'}), 500, {'ContentType':'application/json'}

# ~ @app.route('/api/template', methods = ['POST'])    
# ~ @login_required
# ~ @ownsid
# ~ def add_template():
    # ~ try:
        # ~ if not request.json:
            # ~ abort(400)
        # ~ if not valid_new_domain_dict(request.json):
            # ~ abort(400)     
        # ~ if not app.isardlib.has_access(current_user,request.json['template']):
            # ~ abort(400)                                      
        # ~ if app.isardlib.desktop_add(current_user,request.json['template'],request.json['data']):
            # ~ return jsonify({})
        # ~ return json.dumps({'error': 'Unable to create desktop'}), 500, {'ContentType':'application/json'}
        
    # ~ except Exception as e:
        # ~ exc_type, exc_obj, exc_tb = sys.exc_info()
        # ~ fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # ~ log.error(exc_type, fname, exc_tb.tb_lineno)
        # ~ return json.dumps({'error': 'Unable to get desktop data from database'}), 500, {'ContentType':'application/json'}

@app.route('/api/templates/allowed', methods = ['GET'])
@app.route('/api/templates/allowed/<id>', methods = ['GET'])
@login_required
def form_template_info(id=False):
    try:
        if id:
            data = app.isardlib.get_allowed_id(current_user,'domains',id)
        else:
            data = app.isardlib.get_allowed_data(current_user,'domains')
        if data is False:
            abort(404)            
        return jsonify(data)
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.error(exc_type, fname, exc_tb.tb_lineno)
        return json.dumps({'error': 'Unable to get desktop data from database'}), 500, {'ContentType':'application/json'}

