import logging
from api.common.utils import format_levels
from api.common.constants import (IMPACT_ANALYSIS, LINEAGE_ANALYSIS,
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


def queryPathApoc(tx, type_analysis, toplevel, ids, levels):
    depends = "<DEPENDS" if type_analysis == "lineage" else "DEPENDS>"
    query = """\
            MATCH (top:Group {{type: "{toplevel}"}})
            CALL apoc.path.subgraphNodes([{ids}], {{relationshipFilter: "{depends}", labelFilter: "+Resource", limit: 600}}) YIELD node
            CALL apoc.path.expandConfig(node, {{relationshipFilter: "<CONTAINS", labelFilter: "+Group", terminatorNodes: top}}) YIELD path
            RETURN path as p
            """.strip().format(depends=depends, ids=",".join(map(str, ids)), toplevel=toplevel)
    records = tx.run(query)
    return records


def queryPath(tx, type_analysis, toplevel, ids, levels):
    query_path_analysis = LINEAGE_ANALYSIS_LEVELS \
        if type_analysis == "lineage" else IMPACT_ANALYSIS_LEVELS
    query_path_analysis = query_path_analysis.format(
        levels=format_levels(levels))
    query = """\
            MATCH p={query_path_analysis}
            WHERE id(r) IN [{ids}]
            AND NOT id(n) IN [{ids}]
            WITH DISTINCT NODES(p)
            AS Resource
            UNWIND Resource AS X
            WITH DISTINCT X
            LIMIT 300
            MATCH path=(:Group {{type: "{toplevel}"}})-[:CONTAINS*]->(X)
            RETURN path as p
            UNION
            MATCH path=(:Group {{type: "{toplevel}"}})-[:CONTAINS*]->(X)
            WHERE id(X) in [{ids}]
            RETURN path as p
            """.strip().format(query_path_analysis=query_path_analysis,
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


def queryGroupDependencies(tx, group_id):
    query = """
            MATCH p1=(g_ini:Group)-[:CONTAINS*]->(r_ini:Resource)
            WHERE id(g_ini) = {group_id}
            MATCH p2=(r_ini)-[d:DEPENDS]->(g:Resource),
            p3=(g)<-[:CONTAINS*]-(r:Group {{type: g_ini.type}})
            WHERE id(r) <> {group_id_1}
            RETURN distinct(id(r))
            """.format(group_id=group_id, group_id_1=group_id)
    records = tx.run(query)
    return records


def queryGetResourcesFromGroups(tx, group_ids):
    query = """
            MATCH (G:Group{{type:'Table'}})-[:CONTAINS*]->(R:Resource)
            WHERE ID(G) IN [{group_ids}] RETURN DISTINCT id(R)
            """.format(group_ids=",".join(map(str, group_ids)))
    records = tx.run(query)
    return [x["id(R)"] for x in records]


def queryGroupDependenciesFilter(tx, type_analysis, group_id, resource_ids):
    query_path_analysis = LINEAGE_ANALYSIS \
        if type_analysis == "lineage" else IMPACT_ANALYSIS

    query = """
            MATCH p1=(g_ini:Group)-[:CONTAINS*]->(r_ini:Resource)
            WHERE id(g_ini) = {group_id} AND id(r_ini) in [{resource_ids}]
            MATCH p2={query_path_analysis}
            WHERE id(r) in [{resource_ids}]
            MATCH p3=(r)<-[:CONTAINS*]-(g:Group {{type: g_ini.type}})
            WHERE id(g) <> {group_id}
            RETURN distinct(id(g))
            """.format(group_id=group_id,
                       resource_ids=",".join(map(str, resource_ids)),
                       query_path_analysis=query_path_analysis)

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
            WHERE id(r_ini) = {resource_id} AND id(r) in [{resource_ids}]
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
            MATCH path=(n:Group {showtree: "True", type : "Load"})-[:CONTAINS*]->(target:Group{type: "Table"})
            WITH collect(path) as paths
            CALL apoc.convert.toTree(paths) yield value
            RETURN value
            """
    records = tx.run(query)
    return records

def getTopGroups(tx):
    query = """
        MATCH (n:Group)-[:CONTAINS*]->()
        WHERE not ((n)<-[:CONTAINS]-())
        AND not n.select_hidden
        WITH count(n.name) as cnt, n.name as name,
        collect(n)[0] AS n
        RETURN n
    """
    records = tx.run(query)
    return records

def getTopGroupType(tx):
    query = """
        MATCH (ini:Group)-[:CONTAINS*]->()
        WHERE not ((ini)<-[:CONTAINS]-())
        RETURN ini.type as type limit 1
        """
    records = tx.run(query)
    return records

def listGroupContains(tx, group_id):
    query = """
        MATCH (x:Group)
        WHERE id(x) = {group_id}
        WITH x AS x, x.name AS name
        OPTIONAL MATCH p = (n:Group)-[:CONTAINS*]->(x)
        WHERE NOT ((n)<-[:CONTAINS]-())
        WITH (CASE WHEN p IS NULL THEN [x.name] ELSE [n IN nodes(p) | n.name] END)
        AS origin_list, name AS name
        MATCH (x:Group{{name:name}})-[:CONTAINS]->(n)
        WHERE NOT coalesce(n.select_hidden, false)
        WITH origin_list AS origin_list, n AS target_node
        MATCH p = (n:Group)-[:CONTAINS*]->(target_node)
        WHERE NOT ((n)<-[:CONTAINS]-())
        WITH [n IN nodes(p) | n.name][0..-1] AS target_list, origin_list AS origin_list, target_node AS target_node
        MATCH (target_node)
        WHERE target_list = origin_list AND NOT coalesce(target_node.select_hidden, false)
        WITH count(target_node.name) AS cnt, target_node.name AS name, collect(target_node)[0] AS target_node
        RETURN DISTINCT target_node AS n
        """.format(group_id=group_id)
    records = tx.run(query)
    return records

def queryExtenalIds(tx):
    query = """MATCH (n) RETURN n.external_id AS external_id"""
    records = tx.run(query)
    return records
