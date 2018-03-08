from flask import Blueprint, jsonify, request
from api.common.parser import parseBoltRecords, parseWorkflowDependencies
from api.common.query import (queryMatchNode, queryGetNode,
                              buildNodeFilterEqual, queryResourceDependencies,
                              getUuidsFromNodes)
from api.common.utils import resp, checkonlyone
from api.settings.db import get_neo4j_db
from api.settings.auth import auth

resource = Blueprint('resource', __name__)


@resource.route('/resources', methods=['GET'])
@auth.login_required
def index():
    filters = ""
    if request.args:
        filters = buildNodeFilterEqual(request.args.items())
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryMatchNode,
                                                           "Resource",
                                                           filters))
        return jsonify(nodes), 200


@resource.route('/resources/<int:id>', methods=['GET'])
@auth.login_required
def show(id):
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryGetNode,
                                                           "Resource",
                                                           id))
        return jsonify(nodes[0]), 200


@resource.route('/resources/<int:id>/depends', methods=['GET'])
@auth.login_required
def deps(id):
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryGetNode,
                                                           "Resource",
                                                           id))[0]
        lista = session.write_transaction(queryResourceDependencies, id)
        nodes["depends"] = [x["(id(r))"] for x in lista.data()]
        return jsonify(nodes), 200


@resource.route('/resources/workflows/depends', methods=['POST'])
@auth.login_required
def workflowsFromResource():
    error, param = checkonlyone(["struct_id"], request)
    if error:
        return resp(400, error)

    with get_neo4j_db() as session:
        ids = session.write_transaction(getUuidsFromNodes,
                                        ("struct_id", request.json[param]))
        paths = parseWorkflowDependencies(ids, session)
        return jsonify(paths), 200


@resource.route('/resources/exists', methods=['GET'])
@auth.login_required
def verifyResourceExistance():
    resource = request.args.get('resource')

    if not resource:
        return resp(400, 'Not Element Found')

    filters = "WHERE n.struct_id='{}'".format(resource)

    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryMatchNode,
                                                           "Resource",
                                                           filters))
        if nodes:
            return jsonify({"exists": True})
        else:
            return jsonify({"exists": False})
