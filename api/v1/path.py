from flask import Blueprint, jsonify, request
from api.common.parser import parseBoltPathsFlat, parseBoltPathsTree
from api.common.query import queryPath, getUuidsFromNodes
from api.common.utils import checkparams, abort
from api.settings.db import get_neo4j_db
from api.settings.auth import auth

path = Blueprint('path', __name__)


@path.route('/path', methods=['POST'])
@auth.login_required
def index():
    error = checkparams(["toplevel", "levels", "type_analysis"], request)
    if error:
        return abort(400, {'error': error})
    toplevel = request.json['toplevel']
    levels = request.json['levels']
    type_analysis = request.json['type_analysis']
    ids = request.json["uuids"]

    with get_neo4j_db() as session:
        paths = parseBoltPathsFlat(
            session.write_transaction(queryPath, type_analysis,
                                      toplevel, ids, levels),
            type_analysis, toplevel, session)
        return jsonify({"data": {"paths": paths, "uuids": ids}}), 200


@path.route('/path/levels', methods=['POST'])
@auth.login_required
def levelsFromPath():
    levels = request.json['levels']
    struct_id = request.json["struct_id"]

    with get_neo4j_db() as session:
        ids = session.write_transaction(
            getUuidsFromNodes, ("struct_id", struct_id))
        paths = parseBoltPathsTree(ids, levels, session)
        return jsonify({"data": paths}), 200
