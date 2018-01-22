from flask import Blueprint, jsonify, request

from api.app import app
from api.common.parser import parseBoltPathsFlat, parseBoltPathsTree
from api.common.query import queryPath, getUuidsFromNodes, queryPathLevels
from api.common.utils import make_error, checkparams, checkonlyone
from api.settings.db import get_db


path = Blueprint('path', __name__)

@path.route('/path', methods=['POST'])
def index():
    """
    Path API
    Call this api passing a list of resources ids and get back its paths
    ---
    tags:
      - Path API
    definitions:
      Path:
        type: object
        properties:
          name: ids
          type: array
          items:
            type: int
    parameters:
      - name: titulo
        in: body
        required: true
        description: A list of resources "titulo"
        schema:
          titulo:
            type: array
            description: The Resources childs
            items:
              type: string
    responses:
      400:
        description: Error Ids not found
      200:
        description: A list of paths with its childs
        schema:
          id: Resource id
          properties:
            id:
              type: int
              description: The Resource Id
              default: 1
            tipo:
              type: string
              description: The Resource type
              default: "MAPPING"
            titulo:
              type: string
              description: The Resourcesname
              default: "The awesomeness name"
            contains:
              type: array
              description: The Resources childs
              items:
                type: string
              default: ["resource_contains1", "resource_contains2"]
    """
    error, param = checkonlyone(["uuids", "titles"], request)
    if error:
        return make_error(400, error)
    error = checkparams(["toplevel", "levels"], request)
    if error:
        return make_error(400, error)
    toplevel = request.json['toplevel']
    levels = request.json['levels']
    if param == "titles":
        with get_db() as session:
            ids = session.write_transaction(getUuidsFromNodes, ("struct_id", request.json[param]))
            print(ids)
            paths = parseBoltPathsFlat(session.write_transaction(queryPath, toplevel, ids, levels), ids, toplevel, session)
            return jsonify({ "paths" : paths, "uuids" : ids }), 200
    ids = request.json[param]
    with get_db() as session:
        paths = parseBoltPathsFlat(session.write_transaction(queryPath, toplevel, ids, levels), ids, toplevel, session)
        return jsonify({ "paths" : paths, "uuids" : ids }), 200

@path.route('/path/levels', methods=['POST'])
def levelsFromPath():
    error, param = checkonlyone(["struct_id"], request)
    if error:
        return make_error(400, error)

    error = checkparams(["levels"], request)
    if error:
        return make_error(400, error)
    levels = request.json['levels']

    with get_db() as session:
        ids = session.write_transaction(getUuidsFromNodes, ("struct_id", request.json[param]))
        paths = parseBoltPathsTree(ids, levels, session)
        return jsonify(paths), 200
