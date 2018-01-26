from flask import Blueprint, jsonify, request

from api.app import app
from api.common.query import (queryMatchNode, queryMatchType, queryGetNode, buildNodeFilterEqual,
                              queryGroupDependencies, queryGroupContains, queryGroupTree)
from api.common.parser import parseBoltRecords
from api.settings.db import get_neo4j_db
from api.settings.auth import auth


group = Blueprint('group', __name__)

@group.route('/groups', methods=['GET'])
@auth.login_required
def index():
    """
    Groups API
    ---
    tags:
      - Groups API
    responses:
      200:
        description: A list of Groups
        schema:
          id: group_id
          properties:
            id:
              type: int
              description: The Group Id
              default: 1
            tipo:
              type: string
              description: The Group type
              default: "GROUP"
            titulo:
              type: string
              description: The Group name
              default: "The awesomeness name"
    """
    filters = ""
    if request.args:
        filters = buildNodeFilterEqual(request.args.items())
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryMatchNode,
                                                          "Grupo",
                                                          filters))
        return jsonify(nodes), 200

@group.route('/groups/<int:id>', methods=['GET'])
@auth.login_required
def show(id):
    """
    Group API
    Call this api passing a group id get back its features
    ---
    tags:
      - Groups API
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The group id
    responses:
      200:
        description: A group with its features
        schema:
          id: group_id
          properties:
            id:
              type: int
              description: The Group Id
              default: 1
            tipo:
              type: string
              description: The Group type
              default: "TABLA"
            titulo:
              type: string
              description: The Group name
              default: "The awesomeness name"
    """
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryGetNode,
                                                         "Grupo",
                                                         id))
        return jsonify(nodes[0]), 200

@group.route('/groups/<int:id>/depends', methods=['GET'])
@auth.login_required
def deps(id):
    """
    Group API
    Call this api passing a group id get back its dependencies
    ---
    tags:
      - Groups API
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The group id
    responses:
      200:
        description: A group with its dependencies
        schema:
          id: group_id
          properties:
            id:
              type: int
              description: The Group Id
              default: 1
            tipo:
              type: string
              description: The Group type
              default: "TABLA"
            titulo:
              type: string
              description: The Group name
              default: "The awesomeness name"
            depends:
              type: array
              description: List of Resources
              default: [1, 4, 48]
    """
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryGetNode,
                                                         "Grupo",
                                                         id))[0]
        lista = session.write_transaction(queryGroupDependencies, id)
        nodes["depends"] = [x["(id(r))"] for x in lista.data()]
        return jsonify(nodes), 200

@group.route('/groups/<int:id>/contains', methods=['GET'])
@auth.login_required
def contains(id):
    """
    Group API
    Call this api passing a group id get back its contains
    ---
    tags:
      - Groups API
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The group id
    responses:
      200:
        description: A group with its contains
        schema:
          id: group_id
          properties:
            id:
              type: int
              description: The Group Id
              default: 1
            tipo:
              type: string
              description: The Group type
              default: "TABLA"
            titulo:
              type: string
              description: The Group name
              default: "The awesomeness name"
            contains:
              type: string
              description: List of Resources
              default: "args"
    """
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryGetNode,
                                                         "Grupo",
                                                         id))[0]
        lista = session.write_transaction(queryGroupContains, id)
        nodes["contains"] = [x["(id(r))"] for x in lista.data()]
        return jsonify(nodes), 200

@group.route('/groups/types', methods=['GET'])
@auth.login_required
def typeGroups():
   """
    Groups API
    ---
    tags:
      - Groups API
    responses:
      200:
        description: A list of Groups' types
        schema:
          type: The type of the group
   """
   nodes = {}

   with get_neo4j_db() as session:
       lista = session.write_transaction(queryMatchType,"Grupo")
       nodes["types"] = [x["tipo"] for x in lista.data()]
       return jsonify(nodes), 200

@group.route('/groups/tree', methods=['GET'])
@auth.login_required
def treeGroups():
   """
    Groups API
    ---
    tags:
      - Groups API
    responses:
      200:
        description: Return a navigation groups tree
        schema:
          type: json
   """
   nodes = {}

   with get_neo4j_db() as session:
       result  = session.write_transaction(queryGroupTree)
       nodes["tree"] = [x["value"] for x in result.data()]
       return jsonify(nodes), 200
