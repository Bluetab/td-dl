from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from api.settings.auth import auth
from api.common.utils import abort
from api.app import app
import subprocess
import os

upload = Blueprint('upload', __name__)

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']


@upload.route('/upload', methods=['POST'])
@auth.login_required
def uploadFiles():

    list_filenames = []

    for key_type_file in request.files.keys():
        if 'nodes' in key_type_file or 'rels' in key_type_file:
            list_filenames.extend(
                checkFiles(request.files.getlist(key_type_file), key_type_file)
                )

    string_concat = ";".join(list_filenames)
    status = subprocess.call(['./scripts/importDBNeo4j.sh', string_concat])
    if status != 0:
        abort(422, {'message': "unprocessable entity"})
    return jsonify({"data": {'message': "uploaded"}}), 201


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def checkFiles(list_file_request, type_file):

    list_filenames = []
    for f in list_file_request:
        filename = secure_filename(f.filename)
        if f and allowed_file(filename):
            path_upload = os.path.join(app.config['UPLOAD_FOLDER'],
                                       type_file + '_' + filename)
            list_filenames.append(path_upload)
            f.save(path_upload)

    return list_filenames
