# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, current_app
from api.common.parser import parseBoltPathsFlat, parseBoltPathsTree
from api.common.query import queryPath, queryPathApoc, getUuidsFromNodes
from api.common.utils import checkparams, abort, checkonlyone
from api.settings.db import get_neo4j_db
from api.settings.auth import auth

path = Blueprint('path', __name__)


@path.route('/path', methods=['POST'])
@auth.login_required
def index():
    error, param = checkonlyone(["uuids", "titles"], request)
    if error:
        return abort(400, {'error': error})
    error = checkparams(["levels", "type_analysis"], request)
    if error:
        return abort(400, {'error': error})
    levels = request.json['levels']
    type_analysis = request.json['type_analysis']
    if param == "titles":
        with get_neo4j_db() as session:
            ids = session.write_transaction(getUuidsFromNodes, ("external_id", request.json[param]))
            paths = parseBoltPathsFlat(
                session.write_transaction(queryPath, type_analysis, ids, levels), type_analysis, session)
            return jsonify({"data": {"paths": paths, "uuids": ids}}), 200

    ids = request.json["uuids"]
    with get_neo4j_db() as session:
        unit = queryPathApoc if current_app.config["APOC"] else queryPath
        paths = parseBoltPathsFlat(
            session.write_transaction(unit, type_analysis, ids, levels), type_analysis, session)
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
