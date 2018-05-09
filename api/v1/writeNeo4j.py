from flask import Blueprint, request, jsonify
from api.common.parser import parseBoltRecords
from api.common.utils import checkparams, abort
from api.settings.db import get_neo4j_db
from api.settings.auth import auth
from neo4j import exceptions

writeNeo4j = Blueprint('writeNeo4j', __name__)

@writeNeo4j.route('/writeNeo4j', methods=['POST'])
@auth.login_required
def writeQuery():
    try:
        with get_neo4j_db() as session:
            result = session.run(request.json['query'])
    except exceptions.ConstraintError as exception:
        return abort(400, {'Exception message': exception.message})
    except exceptions.CypherSyntaxError as exception:
        return abort(400, {'Exception message': exception.message})
    except exceptions.CypherTypeError as exception:
        return abort(400, {'Exception message': exception.message})
    except:
        return abort(400, {'Exception message': 'Unknown Error'})
    return "", 204
