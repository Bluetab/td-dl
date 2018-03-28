import os

RESOURCE = "Resource"
GROUP = "Group"

NODES = "nodes"
RELS = "rels"

API_SESSIONS="http://localhost:4003/api/lineage/sessions"
API_UPLOAD="http://localhost:4003/api/lineage/upload"
API_PATH="http://localhost:4003/api/lineage/path"
API_RESOURCES="http://localhost:4003/api/lineage/resources"
API_GROUPS="http://localhost:4003/api/lineage/groups"

HEADERS = {'content-type': 'application/json'}
USER_APP_ADMIN = {"user": {"user_name": "app-admin", "password": "mypass"}}

MAP_RESPONSE = {201: 'Created'}

FILENAME_GROUPS = "groups.csv"
FILENAME_RESOURCES = "resources.csv"
FILENAME_RELATIONS = "relations.csv"
PATH = os.getcwd()


def get_header(token):
    HEADERS_AUTH = HEADERS
    HEADERS_AUTH.update(
        {'Authorization': 'Bearer {token}'.format(token=token)})
    return HEADERS_AUTH


def get_auth_header(token):
    return {'Authorization': 'Bearer {token}'.format(token=token)}
