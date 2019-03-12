# Copyright 2017 the Isard-vdi project authors:
#      Josep Maria Viñolas Auquer
#      Alberto Larraz Dalmases
# License: AGPLv3

from functools import wraps
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_login import current_user

from webapp import app

def ownsid(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_user.role == 'admin': return fn(*args, **kwargs)
        if not 'id' in kwargs.keys(): return make_response(jsonify( { 'error': 'Bad request' } ), 400)
        if not app.isardlib.owns_id(current_user,kwargs['id']): return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
        return fn(*args, **kwargs)
    return decorated_view

#~ def checkRole(fn):
    #~ @wraps(fn)
    #~ def decorated_view(*args, **kwargs):
        #~ if current_user.role == 'user': return redirect(url_for('desktops'))
        #~ return fn(*args, **kwargs)
    #~ return decorated_view
