def queryMatchNode(tx, node, filters="", limit=25):
    records = tx.run("""MATCH (n:%s)
                        %s
                        RETURN n LIMIT %s""" %(node, filters, limit))
    return records

def queryGetResource(tx, ids):
    query = """
            MATCH (n:Recurso) WHERE id(n) IN [{ids}] RETURN n
            """.format(ids=",".join(map(str, ids)))
    records = tx.run(query)
    return records

def queryMatchType(tx, node):
    records = tx.run("""MATCH (G:%s)
                        WITH DISTINCT G.tipo AS tipo
                        RETURN tipo""" %(node))
    return records


def queryGetNode(tx, node, node_id, limit=25):
    records = tx.run("""MATCH (n:%s)
                        WHERE id(n) = %s
                        RETURN n
                        LIMIT %s""" %(node, node_id, limit))
    return records

def queryPath(tx, toplevel, ids, levels):
    if levels == -1:
        format_levels = "*"
    else:
        format_levels = "*1..{levels}".format(levels=levels)
    query = """
            MATCH p=(r:Recurso)<-[D:DEPENDE{levels}{{TARGET_ID:id(r)}}]-(n:Recurso)
            WHERE id(r) in [{ids}] WITH DISTINCT NODES(p) AS RECURSOS UNWIND RECURSOS AS X
            MATCH path=(:Grupo {{tipo: "{toplevel}"}})-[:AGRUPA*]->(X)
            RETURN path as p
            UNION
            MATCH path=(:Grupo {{tipo: "{toplevel}"}})-[:AGRUPA*]->(X)
            WHERE id(X) in [{ids}]
            RETURN path as p
            """.format(levels=format_levels, ids=",".join(map(str, ids)), toplevel=toplevel)
    print(query)
    records = tx.run(query)
    return records

def queryPathLevels(tx, ids, levels):
    if levels == -1:
        format_levels = "*"
    else:
        format_levels = "*1..{levels}".format(levels=levels)
    query = """
            MATCH path=(r:Recurso)<-[:DEPENDE{levels}{{TARGET_ID:id(r)}}]-(n:Recurso)
            WHERE id(r) in [{ids}] WITH collect(path) as paths
            CALL apoc.convert.toTree(paths) yield value
            RETURN value
            """.format(levels=format_levels, ids=",".join(map(str, ids)))

    records = tx.run(query)
    return records

def buildNodeFilterEqual(tupleList):
    filters = ""
    for i, value in enumerate(tupleList):
        if i==0:
            filters += "WHERE n.%s='%s'" %(value[0], value[1])
            continue
        filters += " AND n.%s='%s'" %(value[0], value[1])
    return filters

def queryDependsWorkflow(tx, ids):
    query = """ MATCH (R:Recurso)-[B:BELONGS]->(TG:Recurso{{tipo:'Workflow'}})
    WHERE ID(R) IN [{ids}] RETURN DISTINCT TG AS n
    """.format(ids=",".join(map(str, ids)))
    records = tx.run(query)
    return records

def queryGroupDependencies(tx, group_id):
    query = """MATCH p1=(g_ini:Grupo)-[:AGRUPA*]->(r_ini:Recurso)
               WHERE id(g_ini) = %d
               MATCH p2=(r_ini)-[d:DEPENDE]->(g:Recurso),
               p3=(g)<-[:AGRUPA*]-(r:Grupo {tipo: g_ini.tipo})
               WHERE id(r) <> %d
               RETURN distinct(id(r))""" % (group_id, group_id)
    records = tx.run(query)
    return records

def queryGroupDependenciesFilter(tx, ids, group_id, resource_ids):
    query = """
            MATCH p1=(g_ini:Grupo)-[:AGRUPA*]->(r_ini:Recurso)
            WHERE id(g_ini) = {group_id} AND id(r_ini) in [{resource_ids}]
            MATCH p2=(r_ini)-[d:DEPENDE]->(g:Recurso)
            WHERE id(g) in [{resource_ids}] and d.TARGET_ID in [{ids}]
            MATCH p3=(g)<-[:AGRUPA*]-(r:Grupo {{tipo: g_ini.tipo}})
            WHERE id(r) <> {group_id}
            RETURN distinct(id(r))
            """.format(group_id=group_id, resource_ids=",".join(map(str, resource_ids)), ids=",".join(map(str, ids)))
    records = tx.run(query)
    return records

def queryGroupContains(tx, group_id):
    query = """MATCH p1=(g_ini:Grupo)-[:AGRUPA]->(r)
               WHERE id(g_ini) = %d
               RETURN distinct(id(r))""" % group_id
    records = tx.run(query)
    return records

def queryResourceDependencies(tx, resource_id):
    query = """MATCH p=(g_ini:Recurso)-[:DEPENDE]->(r:Recurso)
               WHERE id(g_ini) = %d
               RETURN distinct(id(r))""" % resource_id
    records = tx.run(query)
    return records

def queryResourceDependenciesFilter(tx, ids, resource_id, resource_ids):
    query = """
            MATCH p=(g_ini:Recurso)-[d:DEPENDE]->(r:Recurso)
            WHERE id(g_ini) = {} AND id(r) in [{}] and d.TARGET_ID in [{ids}]
            RETURN distinct(id(r))
            """.format(resource_id, ",".join(map(str, resource_ids)), ids=",".join(map(str, ids)))
    records = tx.run(query)
    return records

def queryResourceDependenciesNodesFilter(tx, ids, resource_ids):
    query = """
            MATCH (n:Recurso)-[d:DEPENDE]->(r:Recurso)
            WHERE id(r) in [{resource_ids}] and d.TARGET_ID in [{ids}]
            RETURN DISTINCT n
            """.format(resource_ids=",".join(map(str, resource_ids)), ids=",".join(map(str, ids)))

    records = tx.run(query)
    return records

def queryGetGroupsFromResource(tx, resource_id):
    query = """
    MATCH(G:Grupo)-[A:AGRUPA]->(R:Recurso) WHERE ID(R) = {} WITH G as n
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
            MATCH (n:Recurso)
            where toUpper(n.{prop}) =~ toUpper('.*{value}.*')
            return n limit {limit};
            """.format(prop=prop, value=value, limit=limit)
    records = tx.run(query)
    return records

def queryGroupTree(tx):
    query = """
            MATCH path=(n:Grupo {showtree: "True"})-[:AGRUPA*]->(:Recurso)
            WITH collect(path) as paths
            CALL apoc.convert.toTree(paths) yield value
            RETURN value
            """
    records = tx.run(query)
    return records
