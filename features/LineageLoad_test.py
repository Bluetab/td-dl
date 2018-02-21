from lettuce import *
import requests
import pandas
import json

MAP_RESPONSE = {201: 'Created'}

@step('"(.*)" tries to load lineage data with following data:')
def triesToLoad(step, username):

    df_groups = pandas.DataFrame([])
    df_resources = pandas.DataFrame([])
    df_relations = pandas.DataFrame([])

    for row in step.hashes:
        if row.get("File") == 'Resources':
            df_temp = pandas.DataFrame(data={'external_id:ID': [row.get("Id")], \
                'name': [row.get("Name")], 'type': [row.get("Type")], \
                'description': [row.get("Description")], \
                ':LABEL': ['Resources']})
            df_resources = appendDataFrame(df_resources, df_temp)

        elif row.get("File") == 'Groups':
            df_temp = pandas.DataFrame(data={'external_id:ID': [row.get("Id")], \
                'name': [row.get("Name")], 'type': [row.get("Type")], \
                'description': [row.get("Description")], \
                'showtree': [row.get("Showtree")], \
                ':LABEL': ['Groups']})
            df_groups = appendDataFrame(df_groups, df_temp)

        elif row.get("File") == 'Relations':
            df_temp = pandas.DataFrame(data={':START_ID': [row.get("Id Source")], \
                ':END_ID': [row.get("Id Target")], ':TYPE': [row.get("Type")]})
            df_relations = appendDataFrame(df_relations, df_temp)

    df_resources.to_csv('ResourcesPrueba.csv', index = None, sep=';', encoding='utf-8')
    df_groups.to_csv('GroupsPrueba.csv', index = None, sep=';', encoding='utf-8')
    df_relations.to_csv('RelationsPrueba.csv', index = None, sep=';', encoding='utf-8')

    url = 'http://localhost:5000/api/lineage/upload'
    files = [('nodes', open('GroupsPrueba.csv', 'rb')),
        ('nodes', open('ResourcesPrueba.csv', 'rb')),
        ('rels', open('RelationsPrueba.csv', 'rb'))]
    r = requests.post(url, files=files)
    world.status_code = r.status_code

@step(u'Then the system returns a result with code "([^"]*)"')
def then_the_system_returns_a_result_with_code_group1(step, code):
        assert MAP_RESPONSE[world.status_code] == code

@step(u'And "([^"]*)" is able to view following lineage for Resource with Id "([^"]*)" and top level Group type "([^"]*)"')
def and_group1_is_able_to_view_following_lineage_for_resource_with_id_group2_and_top_level_group_type_group3(step, username, resourceId, groupType):
    r = callAPIResources()
    resource = findByKeyJson(r.json(), resourceId, 'external_id')
    assert resource['uuid'] == 4

    url = 'http://localhost:5000/api/lineage/path'
    data = {"uuids":[resource['uuid']], "toplevel":groupType, "levels": -1}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    jsonData = r.json()

    for row in step.hashes:
        object_json = findByKeyJson(jsonData['paths'], row.get("Id"), 'external_id')
        #assert False, "JSON: %s" % object_json
        assert object_json['name'] == row.get("Name")
        assert object_json['type'] == row.get("Type")
        assert object_json['description'] == row.get("Description"), "JSON: %s" % object_json
        if row.get("Contains"):
            findArrayJsonValues(object_json, 'contains', row.get("Contains"))
        findArrayJsonValues(object_json, 'depends', row.get("Depends"))

def findArrayJsonValues(object_json, findKey, findKeyFeatures):
    for valueJson in object_json[findKey]:
        object_find = findByKeyJson(callAPIResources().json(), valueJson, 'uuid')
        try:
            indexvalue = findKeyFeatures.split(",").index(object_find['external_id']), "Got %s" % object_find['external_id']
        except Exception as e:
            assert False, "Value not find %s" %e

def callAPIResources():
    url = 'http://localhost:5000/api/lineage/resources'
    r = requests.get(url)

    return r

def findByKeyJson(json, value, findKey):
    object_json=None

    for x in json:
        if x[findKey] == value:
            object_json = x

    return object_json

def appendDataFrame(df, df_temp):
    if df.empty:
        df = df_temp
    else:
        df = df.append(df_temp)

    return df
