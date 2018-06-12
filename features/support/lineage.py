# -*- coding: utf-8 -*-
from support import constants
from api.app import app
import requests
import pandas
import jwt
import csv


def createFilesAndUpload(context):

    df_groups = pandas.DataFrame([])
    df_resources = pandas.DataFrame([])
    df_relations = pandas.DataFrame([])

    for row in context.table:
        if row["File"] == 'Resources':
            df_temp = pandas.DataFrame(data={
                'external_id:ID': [row["Id"]],
                'name': [row["Name"]], 'type': [row["Type"]],
                'description': [row["Description"]],
                'select_hidden:boolean': [row["Select Hidden"]],
                ':LABEL': ['Resource']})
            df_resources = appendDataFrame(df_resources, df_temp)

        elif row["File"] == 'Groups':
            df_temp = pandas.DataFrame(data={
                'external_id:ID': [row["Id"]],
                'name': [row["Name"]], 'type': [row["Type"]],
                'description': [row["Description"]],
                'select_hidden:boolean': [row["Select Hidden"]],
                ':LABEL': ['Group']})
            df_groups = appendDataFrame(df_groups, df_temp)

        elif row["File"] == 'Relations':
            df_temp = pandas.DataFrame(data={
                ':START_ID': [row["Id Source"]],
                ':END_ID': [row["Id Target"]], ':TYPE': [row["Type"]]})
            df_relations = appendDataFrame(df_relations, df_temp)

    df_resources.to_csv(constants.FILENAME_RESOURCES,
                        index=None, sep=';', encoding='utf-8', quoting=csv.QUOTE_ALL)
    df_groups.to_csv(constants.FILENAME_GROUPS,
                     index=None, sep=';', encoding='utf-8', quoting=csv.QUOTE_ALL)
    df_relations.to_csv(constants.FILENAME_RELATIONS,
                        index=None, sep=';', encoding='utf-8', quoting=csv.QUOTE_ALL)

    files = [
        (constants.NODES,
            open(constants.PATH + "/" + constants.FILENAME_GROUPS, 'rb')),
        (constants.NODES,
            open(constants.PATH + "/" + constants.FILENAME_RESOURCES, 'rb')),
        (constants.RELS,
            open(constants.PATH + "/" + constants.FILENAME_RELATIONS, 'rb'))]

    request = requests.post(constants.API_UPLOAD,
                            files=files,
                            headers=constants.get_auth_header(context.token))

    return request


def check_table_json(context, jsonData):

    for row in context.table:
        object_json = findByKeyJson(jsonData, row["Id"], 'external_id')
        # assert False, "JSON: %s" % object_json
        assert object_json['name'] == row["Name"]
        assert object_json['type'] == row["Type"]
        assert object_json['description'] == row["Description"], \
            "JSON: %s" % object_json
        if "Contains" in row and row["Contains"]:
            findArrayJsonValues(context.token,
                                object_json, 'contains', row["Contains"])
        if "Depends" in row and row["Depends"]:
            findArrayJsonValues(context.token,
                                object_json, 'depends', row["Depends"])


def appendDataFrame(df, df_temp):
    df = df_temp if df.empty else df.append(df_temp)
    return df


def findArrayJsonValues(token, object_json, findKey, findKeyFeatures):
    for valueJson in object_json[findKey]:
        object_find = findByKeyJson(
            callAPIResources(token).json()["data"] +
            callAPIGroups(token).json()["data"], valueJson, 'uuid')
        try:
            indexvalue = findKeyFeatures.split(",") \
                                        .index(object_find['external_id']), \
                                        "Got %s" % object_find['external_id']
            assert indexvalue == object_find['external_id']
        except Exception as e:
            assert False, "Value not find %s" % e


def callAPIResources(token):
    r = requests.get(constants.API_RESOURCES,
                     headers=constants.get_auth_header(token))
    return r


def callAPIGroups(token):
    r = requests.get(constants.API_GROUPS,
                     headers=constants.get_auth_header(token))
    return r


def findByKeyJson(json, value, findKey):
    object_json = None

    for x in json:
        if x[findKey] == value:
            object_json = x

    return object_json


def buildToken(user):
    user['user']['aud'] = app.config['JWT_AUD']
    token = jwt.encode(user['user'],
                       app.config['SECRET_KEY'],
                       app.config['ALGORITHM']).decode("utf-8")
    return token

# def buildDeleteQuery(node_id):
#     def queryMatchNode(tx, node, filters="", limit=25):
#         query = """
#                 MATCH (n:{node})
#                 {filters}
#                 RETURN n LIMIT {limit}
#                 """.format(node=node, filters=filters, limit=limit)
#         records = tx.run(query)
#         return records
