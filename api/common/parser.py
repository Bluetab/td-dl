from api.common.utils import findIndexInList
from api.common.query import (queryGroupDependenciesFilter, queryResourceDependenciesFilter,
queryGetResource, queryResourceDependenciesNodesFilter, queryDependsWorkflow, queryGetGroupsFromResource)
from api.settings.db import get_neo4j_db
import json

def parseBoltNodes(node):
    n = {}
    n['uuid'] = node.id
    n['labels'] = list(node.labels)
    for k in node:
        n[k] = node[k]
    return n

def parseBoltRecords(records):
    nodes = []
    for record in records:
        r = parseBoltNodes(record["n"])
        nodes.append(r)
    return nodes

def getDepsNodes(node, ids, resource_ids, session):
    if "Grupo" in node["labels"]:
        lista = session.write_transaction(queryGroupDependenciesFilter, ids, node["uuid"], resource_ids)
        node["depends"] = [x["(id(r))"] for x in lista.data()]
    elif "Recurso" in node["labels"]:
        lista = session.write_transaction(queryResourceDependenciesFilter, ids, node["uuid"], resource_ids)
        node["depends"] = [x["(id(r))"] for x in lista.data()]
    return node

def parseBoltPathsFlat(records, ids, toplevel, session):
    records = records.data()
    nodes = list(set([item for sublist in map(lambda x: x["p"].nodes, records) for item in sublist]))
    nodes = [parseBoltNodes(x) for x in nodes]
    for record in records:
        deep = 0
        path = record["p"]
        for p in path:
            start_id = findIndexInList(nodes, lambda item: item["uuid"] == p.start)
            contains = nodes[start_id].setdefault("contains", [])
            if not p.end in contains:
                contains.append(p.end)
            nodes[start_id]["depth"] = deep
            deep += 1
    # Add dependencies
    resource_ids = list(map(lambda x: x["uuid"], filter(lambda x: "Recurso" in x["labels"], nodes)))
    nodes = [getDepsNodes(x, ids, resource_ids, session) for x in nodes]
    return nodes

def verifyAlreadyExists(records, levelsMap):
    for key, value in levelsMap.items():
        records = [x for x in records if x not in levelsMap[key]]
    return records

def getGroupDependencies(records, session):
    for node in records:
        arrayGroups = parseBoltRecords(queryGetGroupsFromResource(session, node['uuid']))
        node['groups'] = [x['titulo'] for x in arrayGroups]

    return records

def parseBoltPathsTree(ids, levels, session):
    result = []

    for idNode in ids:
        idsToQuery = [idNode]
        index = 1
        levelsMap = {}
        resultNodes = parseBoltRecords(queryGetResource(session, [idNode]))

        idsToQuery = [x["uuid"] for x in resultNodes]

        levelsMap[index] = getGroupDependencies(resultNodes, session)

        if levels != -1:
             while index < int(levels):
                 resultNodes = verifyAlreadyExists(parseBoltRecords(queryResourceDependenciesNodesFilter(session, [idNode], idsToQuery)), levelsMap)
                 idsToQuery = [x["uuid"] for x in resultNodes]
                 index = index + 1
                 levelsMap[index] = getGroupDependencies(resultNodes, session)
        else:
            while idsToQuery:
                resultNodes = verifyAlreadyExists(parseBoltRecords(queryResourceDependenciesNodesFilter(session, [idNode], idsToQuery)), levelsMap)
                idsToQuery = [x["uuid"] for x in resultNodes]
                index = index + 1
                levelsMap[index] = getGroupDependencies(resultNodes, session)

        result.append( levelsMap )

    return { "tables" : result }

def parseWorkflowDependencies(ids, session):

    responseMap = {}

    for idNode in ids:
        resultNode = parseBoltRecords(queryGetResource(session, [idNode]))
        workflows = parseBoltRecords(queryDependsWorkflow(session, [idNode]))
        responseMap[resultNode[0]["struct_id"]] = workflows

    return { "result" : responseMap }
