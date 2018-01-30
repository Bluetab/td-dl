from flask import Blueprint, jsonify, request
from api.common.parser import parseBoltPathsFlat, parseBoltPathsTree
from api.common.query import queryPath, getUuidsFromNodes
from api.common.utils import make_error, checkparams, checkonlyone
from api.settings.db import get_neo4j_db


path = Blueprint('path', __name__)


@path.route('/path', methods=['POST'])
def index():
    error, param = checkonlyone(["uuids", "titles"], request)
    if error:
        return make_error(400, error)
    error = checkparams(["toplevel", "levels"], request)
    if error:
        return make_error(400, error)
    toplevel = request.json['toplevel']
    levels = request.json['levels']
    if param == "titles":
        with get_neo4j_db() as session:
            ids = session.write_transaction(getUuidsFromNodes,
                                            ("struct_id", request.json[param]))
            paths = parseBoltPathsFlat(
                session.write_transaction(queryPath, toplevel, ids, levels),
                ids, toplevel, session)
            return jsonify({"paths": paths, "uuids": ids}), 200
    ids = request.json[param]
    with get_neo4j_db() as session:
        paths = parseBoltPathsFlat(
            session.write_transaction(queryPath, toplevel, ids, levels),
            ids, toplevel, session)
        return jsonify({"paths": paths, "uuids": ids}), 200


@path.route('/path/levels', methods=['POST'])
def levelsFromPath():
    error, param = checkonlyone(["struct_id"], request)
    if error:
        return make_error(400, error)

    error = checkparams(["levels"], request)
    if error:
        return make_error(400, error)
    levels = request.json['levels']

    with get_neo4j_db() as session:
        ids = session.write_transaction(
            getUuidsFromNodes, ("struct_id", request.json[param]))
        paths = parseBoltPathsTree(ids, levels, session)
        return jsonify(paths), 200
