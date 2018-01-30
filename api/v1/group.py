from flask import Blueprint, jsonify, request

from api.common.query import (queryMatchNode, queryMatchType, queryGetNode,
                              buildNodeFilterEqual,
                              queryGroupDependencies, queryGroupContains,
                              queryGroupTree)
from api.common.parser import parseBoltRecords
from api.settings.db import get_neo4j_db
from api.settings.auth import auth


group = Blueprint('group', __name__)


@group.route('/groups', methods=['GET'])
@auth.login_required
def index():
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
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryGetNode,
                                                           "Grupo",
                                                           id))
        return jsonify(nodes[0]), 200


@group.route('/groups/<int:id>/depends', methods=['GET'])
@auth.login_required
def deps(id):
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
    nodes = {}

    with get_neo4j_db() as session:
        lista = session.write_transaction(queryMatchType, "Grupo")
        nodes["types"] = [x["tipo"] for x in lista.data()]
        return jsonify(nodes), 200


@group.route('/groups/tree', methods=['GET'])
@auth.login_required
def treeGroups():
    nodes = {}

    with get_neo4j_db() as session:
        result = session.write_transaction(queryGroupTree)
        nodes["tree"] = [x["value"] for x in result.data()]
        return jsonify(nodes), 200
