from flask import Blueprint, jsonify, request

from api.app import app
from api.common.parser import parseBoltRecords, parseWorkflowDependencies
from api.common.query import (queryMatchNode, queryGetNode, buildNodeFilterEqual,
                              queryResourceDependencies, getUuidsFromNodes)
from api.common.utils import make_error, checkparams, checkonlyone
from api.settings.db import get_neo4j_db


resource = Blueprint('resource', __name__)

@resource.route('/resources', methods=['GET'])
def index():
    """
    Resources API
    ---
    tags:
      - Resources API
    responses:
      200:
        description: A list of Resources
        schema:
          id: Resource_id
          properties:
            id:
              type: int
              description: The Resource Id
              default: 1
            tipo:
              type: string
              description: The Resource type
              default: "TABLA"
            titulo:
              type: string
              description: The Resource name
              default: "The awesomeness name"
    """
    filters = ""
    if request.args:
        filters = buildNodeFilterEqual(request.args.items())
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryMatchNode,
                                                         "Recurso",
                                                         filters))
        return jsonify(nodes), 200

@resource.route('/resources/<int:id>', methods=['GET'])
def show(id):
    """
    Resource API
    Call this api passing a Resource id get back its features
    ---
    tags:
      - Resources API
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The Resource id
    responses:
      200:
        description: A group with its features
        schema:
          id: Resource_id
          properties:
            id:
              type: int
              description: The Resource Id
              default: 1
            tipo:
              type: string
              description: The Resource type
              default: "TABLA"
            titulo:
              type: string
              description: The Resourcesname
              default: "The awesomeness name"
    """
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryGetNode,
                                                         "Recurso",
                                                         id))
        return jsonify(nodes[0]), 200

@resource.route('/resources/<int:id>/depends', methods=['GET'])
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
                                                         "Recurso",
                                                         id))[0]
        lista = session.write_transaction(queryResourceDependencies, id)
        nodes["depends"] = [x["(id(r))"] for x in lista.data()]
        return jsonify(nodes), 200

@resource.route('/resources/workflows/depends', methods=['POST'])
def workflowsFromResource():
    error, param = checkonlyone(["struct_id"], request)
    if error:
        return make_error(400, error)

    with get_neo4j_db() as session:
        ids = session.write_transaction(getUuidsFromNodes, ("struct_id", request.json[param]))
        paths = parseWorkflowDependencies(ids, session)
        return jsonify(paths), 200

@resource.route('/resources/exists', methods=['GET'])
def verifyResourceExistance():
    resource = request.args.get('resource')

    if not resource:
        return make_error(400, 'Not Element Found')

    filters="WHERE n.struct_id='{}'".format(resource)

    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryMatchNode,
                                                         "Recurso",
                                                         filters))
        if nodes:
            return jsonify({ "exists" : True })
        else:
            return jsonify({ "exists" : False })
