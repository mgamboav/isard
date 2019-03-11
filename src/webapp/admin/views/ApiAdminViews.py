# Copyright 2017 the Isard-vdi project authors:
#      Josep Maria Viñolas Auquer
#      Alberto Larraz Dalmases
# License: AGPLv3

#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth

from webapp import app
from ...lib import admin_api

app.adminapi = admin_api.isardAdmin()

from .decorators import isAdmin

# ~ remote_addr=request.headers['X-Forwarded-For'].split(',')[0] if 'X-Forwarded-For' in request.headers else request.remote_addr.split(',')[0]

@app.route('/api/<table>', methods = ['GET'])    
@app.route('/api/<table>/<id>', methods = ['GET'])
@login_required
@isAdmin
def get_from_table(table,id=False):
    try:
        pluck = request.args.get('pluck', default = *, type = str)
        order = request.args.get('order', default = '*', type = str)    
    except:
        pluck = False
        order = False
    return jsonify( { table: app.adminapi.get_admin_table(table,id,pluck,order) } )

@app.route('/api/<table>/<id>', methods = ['DELETE'])
@login_required
@isAdmin
def delete_from_table(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify( { 'result': True } )

@app.route('/api/<table>', methods = ['POST'])    
@login_required
@isAdmin
def add_to_table():
    if not request.json or :
        abort(400)
    if type(request.json['title']) != unicode:
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify( { 'task': make_public_task(task) } ), 201

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
    

    
