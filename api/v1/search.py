from flask import Blueprint, jsonify, request
from api.common.query import searchResourceReg
from api.settings.db import get_neo4j_db
from api.common.parser import parseBoltRecords
from api.common.utils import findInArgs, make_error

search = Blueprint('search', __name__)


@search.route('/search', methods=['GET'])
def index():
    if not request.args:
        return make_error(400, "Error args not found")
    error, keyvalue = findInArgs("title", request.args)
    if error:
        return make_error(400, error)
    with get_neo4j_db() as session:
        nodes = parseBoltRecords(session.write_transaction(searchResourceReg,
                                                           keyvalue[0],
                                                           keyvalue[1]))
        return jsonify(nodes), 200
