from flask import Blueprint, jsonify, request
from api.common.query import searchResourceReg
from api.settings.db import get_db
from api.common.parser import parseBoltRecords
from api.common.utils import findInArgs, make_error

search = Blueprint('search', __name__)

@search.route('/search', methods=['GET'])
def index():
    """
    Search API
    ---
    tags:
      - Search API
    responses:
      200:
        description: A list of Resources
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
    if not request.args:
        return make_error(400, "Error args not found")
    error, keyvalue = findInArgs("titulo", request.args)
    if error:
        return make_error(400, error)
    with get_db() as session:
        nodes = parseBoltRecords(session.write_transaction(searchResourceReg,
                                                          keyvalue[0],
                                                          keyvalue[1]))
        return jsonify(nodes), 200
