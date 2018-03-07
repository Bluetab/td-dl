from api.common.utils import format_levels
from api.settings.constants import (IMPACT_ANALYSIS, LINEAGE_ANALYSIS,
                                    IMPACT_ANALYSIS_LEVELS,
                                    LINEAGE_ANALYSIS_LEVELS)


def queryMatchNode(tx, node, filters="", limit=25):
    query = """
            MATCH (n:{node})
            {filters}
            RETURN n LIMIT {limit}
            """.format(node=node, filters=filters, limit=limit)
    records = tx.run(query)
    return records


def queryGetResource(tx, ids):
    query = """
            MATCH (n:Resource)
            WHERE id(n) IN [{ids}]
            RETURN n
            """.format(ids=",".join(map(str, ids)))
    records = tx.run(query)
    return records


def queryMatchType(tx, node):
    query = """
            MATCH (G:{node})
            WITH DISTINCT G.type AS type
            RETURN type
            """.format(node=node)
    records = tx.run(query)
    return records


def queryGetNode(tx, node, node_id, limit=25):
    query = """
            MATCH (n:{node})
            WHERE id(n) = {node_id}
            RETURN n
            LIMIT {limit}
            """.format(node=node, node_id=node_id, limit=limit)
    records = tx.run(query)
    return records


def queryPath(tx, type_analysis, toplevel, ids, levels):
    query_path_analysis = LINEAGE_ANALYSIS_LEVELS \
        if type_analysis == "lineage" else IMPACT_ANALYSIS_LEVELS
    query_path_analysis = query_path_analysis.format(
        levels=format_levels(levels))
    query = """
            MATCH p={query_path_analysis}
            WHERE id(r) in [{ids}] WITH DISTINCT NODES(p)
            AS Resource UNWIND Resource AS X
            MATCH path=(:Group {{type: "{toplevel}"}})-[:CONTAINS*]->(X)
            RETURN path as p
            UNION
            MATCH path=(:Group {{type: "{toplevel}"}})-[:CONTAINS*]->(X)
            WHERE id(X) in [{ids}]
            RETURN path as p
            """.format(query_path_analysis=query_path_analysis,
                       ids=",".join(map(str, ids)), toplevel=toplevel)
    records = tx.run(query)
    return records


def queryPathLevels(tx, ids, levels):
    query = """
            MATCH path=(r:Resource)<-[:DEPENDS{levels}]-(n:Resource)
            WHERE id(r) in [{ids}] WITH collect(path) as paths
            CALL apoc.convert.toTree(paths) yield value
            RETURN value
            """.format(levels=format_levels(levels),
                       ids=",".join(map(str, ids)))
    records = tx.run(query)
    return records


def buildNodeFilterEqual(tupleList):
    filters = ""
    for i, value in enumerate(tupleList):
        if i == 0:
            filters += "WHERE n.%s='%s'" % (value[0], value[1])
            continue
        filters += " AND n.%s='%s'" % (value[0], value[1])
    return filters


def queryDependsWorkflow(tx, ids):
    query = """
            MATCH (R:Resource)-[B:BELONGS]->(TG:Resource{{tipo:'Workflow'}})
            WHERE ID(R) IN [{ids}]
            RETURN DISTINCT TG AS n
            """.format(ids=",".join(map(str, ids)))
    records = tx.run(query)
    return records


def queryGroupDependencies(tx, group_id):
    query = """
            MATCH p1=(g_ini:Group)-[:CONTAINS*]->(r_ini:Resource)
            WHERE id(g_ini) = {group_id}
            MATCH p2=(r_ini)-[d:DEPENDS]->(g:Resource),
            p3=(g)<-[:CONTAINS*]-(r:Group {tipo: g_ini.tipo})
            WHERE id(r) <> {group_id_1}
            RETURN distinct(id(r))
            """.format(group_id=group_id, group_id_1=group_id)
    records = tx.run(query)
    return records


def queryGetResourcesFromGroups(tx, group_ids):
    query = """
            MATCH (G:Group{{type:'Object'}})-[:CONTAINS*]->(R:Resource)
            WHERE ID(G) IN [{group_ids}] RETURN DISTINCT id(R)
            """.format(group_ids=",".join(map(str, group_ids)))
    records = tx.run(query)
    return [x["id(R)"] for x in records]


def queryGroupDependenciesFilter(tx, group_id, resource_ids):
    query = """
            MATCH p1=(g_ini:Group)-[:CONTAINS*]->(r_ini:Resource)
            WHERE id(g_ini) = {group_id} AND id(r_ini) in [{resource_ids}]
            MATCH p2=(r_ini)-[d:DEPENDS]->(g:Resource)
            WHERE id(g) in [{resource_ids}]
            MATCH p3=(g)<-[:CONTAINS*]-(r:Group {{tipo: g_ini.tipo}})
            WHERE id(r) <> {group_id}
            RETURN distinct(id(r))
            """.format(group_id=group_id,
                       resource_ids=",".join(map(str, resource_ids)))
    records = tx.run(query)
    return records


def queryGroupContains(tx, group_id):
    query = """
            MATCH p1=(g_ini:Group)-[:CONTAINS]->(r)
            WHERE id(g_ini) = %d
            RETURN distinct(id(r))""" % group_id
    records = tx.run(query)
    return records


def queryResourceDependencies(tx, resource_id):
    query = """
            MATCH p=(g_ini:Resource)-[:DEPENDS]->(r:Resource)
            WHERE id(g_ini) = %d
            RETURN distinct(id(r))""" % resource_id
    records = tx.run(query)
    return records


def queryResourceDependenciesFilter(tx, type_analysis,
                                    resource_id, resource_ids):
    query_path_analysis = LINEAGE_ANALYSIS \
        if type_analysis == "lineage" else IMPACT_ANALYSIS
    query = """
            MATCH p={query_path_analysis}
            WHERE id(g_ini) = {resource_id} AND id(r) in [{resource_ids}]
            RETURN distinct(id(r))
            """.format(query_path_analysis=query_path_analysis,
                       resource_id=resource_id,
                       resource_ids=",".join(map(str, resource_ids)))
    records = tx.run(query)
    return records


def queryResourceDependenciesNodesFilter(tx, resource_ids):
    query = """
            MATCH (n:Resource)-[d:DEPENDS]->(r:Resource)
            WHERE id(r) in [{resource_ids}]
            RETURN DISTINCT n
            """.format(resource_ids=",".join(map(str, resource_ids)))

    records = tx.run(query)
    return records


def queryGetGroupsFromResource(tx, resource_id):
    query = """
            MATCH(G:Group)-[A:CONTAINS]->(R:Resource)
            WHERE ID(R) = {} WITH G as n
            RETURN DISTINCT n
            """.format(resource_id)
    records = tx.run(query)
    return records


def getUuidsFromNodes(tx, pro_values):
    query = """
            MATCH (n)
            WHERE n.{} in ['{}']
            RETURN id(n)
            """.format(pro_values[0], "','".join(map(str, pro_values[1])))
    records = tx.run(query)
    return [x["id(n)"] for x in records]


def searchResourceReg(tx, prop, value, limit=25):
    query = """
            MATCH (n:Resource)
            where toUpper(n.{prop}) =~ toUpper('.*{value}.*')
            return n limit {limit};
            """.format(prop=prop, value=value, limit=limit)
    records = tx.run(query)
    return records


def queryGroupTree(tx):
    query = """
            MATCH path=(n:Group {showtree: "True", type : "Load"})-[:CONTAINS*]->(target:Group{type: "Object"})
            WITH collect(path) as paths
            CALL apoc.convert.toTree(paths) yield value
            RETURN value
            """
    records = tx.run(query)
    return records
