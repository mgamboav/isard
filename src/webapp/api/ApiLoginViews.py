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
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
    
@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        au=auth()
        user=au.check(request.form['user'],request.form['password'])
        if user:
            login_user(user)
            if user.auto is not False:
                app.isardapi.new_domains_auto_user(user.username,user.auto)
            return jsonify({})
        return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.error(exc_type, fname, exc_tb.tb_lineno)
        return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
