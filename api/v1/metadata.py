# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from api.settings.auth import auth
from api.settings.db import get_neo4j_db
from api.common.cache import cache_field_external_ids
from api.common.query import queryExtenalIds

from api.common.utils import abort
from api.app import app

import subprocess
import os


metadata = Blueprint('metadata', __name__)

UPLOAD_PATH = app.config['UPLOAD_PATH']
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']
METADATA_SCRIPT = app.config['METADATA_SCRIPT']


@metadata.route('/td_dl/metadata', methods=['POST'])
@auth.login_required
def upload():

    list_filenames = []

    for key_type_file in request.files.keys():
        if 'nodes' in key_type_file or 'rels' in key_type_file:
            list_filenames.extend(
                checkFiles(request.files.getlist(key_type_file), key_type_file)
            )
    if not list_filenames:
        return abort(422, {'message': 'unprocessable entity'})

    if METADATA_SCRIPT:
        string_concat = ';'.join(list_filenames)
        status = subprocess.call([METADATA_SCRIPT, string_concat])
        if status != 0:
            return abort(422, {'message': 'unprocessable entity'})

    return '', 202


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def checkFiles(list_file_request, type_file):
    list_filenames = []
    for f in list_file_request:
        filename = secure_filename(f.filename)
        if f and allowed_file(filename):
            path_upload = os.path.join(UPLOAD_PATH,
                                       type_file + '_' + filename)
            list_filenames.append(path_upload)
            f.save(path_upload)

    return list_filenames


@metadata.route('/td_dl/cache', methods=['POST'])
@auth.login_required
def cache():
    with get_neo4j_db() as session:
        result = session.read_transaction(queryExtenalIds)
        # Cache external_ids with format <system>.<group>.<name>.<field>
        external_ids = [r["external_id"] for r in result if r["external_id"].count(".") == 3]
        cache_field_external_ids(external_ids)
    return '', 204
