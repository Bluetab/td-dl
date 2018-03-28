from api.common.utils import findIndexInList
from api.common.query import (queryGroupDependenciesFilter,
                              queryResourceDependenciesFilter,
                              queryGetResource,
                              queryResourceDependenciesNodesFilter,
                              queryGetGroupsFromResource)


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


def getDepsNodes(node, type_analysis, resource_ids, session):
    if "Group" in node["labels"]:
        lista = session.write_transaction(queryGroupDependenciesFilter,
                                          type_analysis, node["uuid"],
                                          resource_ids)
        node["depends"] = [x["(id(g))"] for x in lista.data()]
    elif "Resource" in node["labels"]:
        lista = session.write_transaction(queryResourceDependenciesFilter,
                                          type_analysis, node["uuid"],
                                          resource_ids)
        node["depends"] = [x["(id(r))"] for x in lista.data()]
    return node


def parseBoltPathsFlat(records, type_analysis, toplevel, session):
    records = records.data()
    nodes = list(set([item for
                      sublist in map(lambda x: x["p"].nodes, records)
                      for item in sublist]))
    nodes = [parseBoltNodes(x) for x in nodes]
    for record in records:
        deep = 0
        path = record["p"]
        for p in path:
            start_id = findIndexInList(nodes,
                                       lambda item: item["uuid"] == p.start)
            contains = nodes[start_id].setdefault("contains", [])
            if p.end not in contains:
                contains.append(p.end)
            nodes[start_id]["depth"] = deep
            deep += 1
    # Add dependencies
    resource_ids = list(map(lambda x: x["uuid"],
                            filter(lambda x: "Resource"
                                   in x["labels"], nodes)))
    nodes = [getDepsNodes(x, type_analysis, resource_ids, session)
             for x in nodes]
    return nodes


def verifyAlreadyExists(records, levelsMap):
    for key, value in levelsMap.items():
        records = [x for x in records if x not in levelsMap[key]]
    return records


def getGroupDependencies(records, session):
    for node in records:
        arrayGroups = parseBoltRecords(queryGetGroupsFromResource(session,
                                                                  node['uuid'])
                                       )
        node['group'] = [x['title'] for x in arrayGroups]

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
                resultNodes = verifyAlreadyExists(parseBoltRecords(
                    queryResourceDependenciesNodesFilter(
                        session, [idNode], idsToQuery)), levelsMap)
                idsToQuery = [x["uuid"] for x in resultNodes]
                index = index + 1
                levelsMap[index] = getGroupDependencies(resultNodes, session)
        else:
            while idsToQuery:
                resultNodes = verifyAlreadyExists(parseBoltRecords(
                    queryResourceDependenciesNodesFilter(
                        session, [idNode], idsToQuery)), levelsMap)
                idsToQuery = [x["uuid"] for x in resultNodes]
                index = index + 1
                levelsMap[index] = getGroupDependencies(resultNodes, session)

        result.append(levelsMap)

    return {"tables": result}
