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
    

@app.route('/api/users/allowed/hardware', methods = ['GET'])
@login_required
def users_allowed_hardware():
    try:
        return jsonify(app.isardlib.user_allowed_hardware(current_user))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.error(exc_type, fname, exc_tb.tb_lineno)
        return json.dumps({'error': 'Unable to get user hardware allowed from database'}), 500, {'ContentType':'application/json'}
