from flask import Blueprint, jsonify, request

from api.common.query import (queryMatchNode, queryMatchType, queryGetNode,
                              buildNodeFilterEqual,
                              queryGroupDependencies, queryGroupContains,
                              queryGroupTree, queryGetResourcesFromGroups,
                              queryPath, getTopGroupType)
from api.common.parser import parseBoltRecords, parseBoltPathsFlat
from api.settings.db import get_neo4j_db
from api.settings.auth import auth
from api.common.utils import resp, checkparams


group = Blueprint('group', __name__)


@group.route('/groups', methods=['GET'])
@auth.login_required
def index():
    filters = ""
    if request.args:
        filters = buildNodeFilterEqual(request.args.items())
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryMatchNode,
                                                           "Group",
                                                           filters))
        return jsonify(nodes), 200


@group.route('/groups/<int:id>', methods=['GET'])
@auth.login_required
def show(id):
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryGetNode,
                                                           "Group",
                                                           id))
        return jsonify(nodes[0]), 200


@group.route('/groups/<int:id>/depends', methods=['GET'])
@auth.login_required
def deps(id):
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryGetNode,
                                                           "Group",
                                                           id))[0]
        lista = session.write_transaction(queryGroupDependencies, id)
        nodes["depends"] = [x["(id(r))"] for x in lista.data()]
        return jsonify(nodes), 200


@group.route('/groups/<int:id>/contains', methods=['GET'])
@auth.login_required
def contains(id):
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(queryGetNode,
                                                           "Group",
                                                           id))[0]
        lista = session.write_transaction(queryGroupContains, id)
        nodes["contains"] = [x["(id(r))"] for x in lista.data()]
        return jsonify(nodes), 200


@group.route('/groups/types', methods=['GET'])
@auth.login_required
def typeGroups():
    nodes = {}

    with get_neo4j_db() as session:
        lista = session.write_transaction(queryMatchType, "Group")
        nodes["types"] = [x["type"] for x in lista.data()]
        return jsonify(nodes), 200


@group.route('/groups/tree', methods=['GET'])
@auth.login_required
def treeGroups():
    nodes = {}

    with get_neo4j_db() as session:
        result = session.write_transaction(queryGroupTree)
        nodes["tree"] = [x["value"] for x in result.data()]
        return jsonify(nodes), 200


@group.route('/groups/path', methods=['POST'])
@auth.login_required
def pathGroups():
    error = checkparams(["toplevel", "levels", "type_analysis"], request)
    if error:
        return resp(400, error)
    toplevel = request.json["toplevel"]
    levels = request.json["levels"]
    type_analysis = request.json["type_analysis"]
    group_ids = request.json["uuids"]

    with get_neo4j_db() as session:
        ids = session.write_transaction(queryGetResourcesFromGroups,
                                        group_ids)
        paths = parseBoltPathsFlat(
            session.write_transaction(queryPath, type_analysis,
                                      toplevel, ids, levels),
            type_analysis, toplevel, session)

    return jsonify({"paths": paths, "uuids": ids}), 200


@group.route('/groups/toptype', methods=['GET'])
@auth.login_required
def topGroup():
    result = {}
    with get_neo4j_db() as session:
        types = session.write_transaction(getTopGroupType)
        result["type"] = [x["type"] for x in types.data()][0]
        return jsonify(result), 200
