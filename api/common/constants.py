PORT_DES = 4003
PORT_PRO = 4003

LINEAGE_ANALYSIS_LEVELS = "(r:Resource)<-[D:DEPENDS{levels}]-(n:Resource)"
IMPACT_ANALYSIS_LEVELS = "(r:Resource)-[D:DEPENDS{levels}]->(n:Resource)"

LINEAGE_ANALYSIS = "(r_ini:Resource)<-[DEPENDS]-(r:Resource)"
IMPACT_ANALYSIS = "(r_ini:Resource)-[DEPENDS]->(r:Resource)"
