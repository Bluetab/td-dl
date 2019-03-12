LINEAGE_ANALYSIS_LEVELS = "(r:Resource)<-[:DEPENDS{levels}]-(n:Resource)"
IMPACT_ANALYSIS_LEVELS = "(r:Resource)-[:DEPENDS{levels}]->(n:Resource)"

LINEAGE_ANALYSIS = "(r_ini:Resource)<-[:DEPENDS]-(r:Resource)"
IMPACT_ANALYSIS = "(r_ini:Resource)-[:DEPENDS]->(r:Resource)"
