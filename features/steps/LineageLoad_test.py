# -*- coding: utf-8 -*-
from behave import when, then, given
from support import constants
from support import lineage
import requests
import json

@when('"{username}" tries to load lineage data with following data')
def step_impl(context, username):

    token = lineage.buildToken(constants.USER_APP_ADMIN)
    context.token = token
    request = lineage.createFilesAndUpload(context)
    context.status_code = request.status_code

@then('the system returns a result with code "{code}"')
def step_impl(context, code):
    assert constants.MAP_RESPONSE[context.status_code] == code

@then('"{username}" is able to view following "{type_analysis}" for Resource with Id "{resourceId}" and top level Group type "{groupType}"')
def step_impl(context, username, type_analysis, resourceId, groupType):
    r = lineage.callAPIResources(context.token)
    resource = lineage.findByKeyJson(r.json()["data"], resourceId, 'external_id')

    data = {"uuids":[resource['uuid']], "toplevel":groupType, "levels": -1, "type_analysis":type_analysis}
    r = requests.post(constants.API_PATH, data=json.dumps(data), headers=constants.get_header(context.token))
    lineage.check_table_json(context, r.json()["data"]['paths'])

@given('following lineage data has been already loaded')
def step_impl(context):
    token = lineage.buildToken(constants.USER_APP_ADMIN)
    context.token = token
    request = lineage.createFilesAndUpload(context)
    context.status_code = request.status_code

@when('"{username}" tries to get the "{type_analysis}" analysis for Resource with Id "{resourceId}" and top level Group type "{groupType}"')
def step_impl(context, username, type_analysis, resourceId, groupType):
    r = lineage.callAPIResources(context.token)
    resource = lineage.findByKeyJson(r.json()["data"], resourceId, 'external_id')

    data = {"uuids":[resource['uuid']], "toplevel":groupType, "levels": -1, "type_analysis":type_analysis}
    r = requests.post(constants.API_PATH, json=data, headers=constants.get_header(context.token))
    context.jsonData = r.json()

@then('he receives following lineage information')
def step_impl(context):
    lineage.check_table_json(context, context.jsonData["data"]['paths'])

@when('"{username}" tries to list Groups with a contains relation with Group Id "{group_id}"')
def step_impl(context, username, group_id):
    r = lineage.callAPIGroups(context.token)
    resource = lineage.findByKeyJson(r.json()["data"], group_id, 'external_id')
    r = requests.get("{0}/{1}/index_contains".format(constants.API_GROUPS, resource['uuid']), headers=constants.get_header(context.token))
    context.jsonData = r.json()

@then('he receives following nodes list')
def step_impl(context):
    lineage.check_table_json(context, context.jsonData["data"])

@when('"{username}" tries to list top Groups')
def step_impl(context, username):
    r = requests.get("{0}/index_top".format(constants.API_GROUPS), headers=constants.get_header(context.token))
    context.jsonData = r.json()
