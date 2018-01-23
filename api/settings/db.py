from flask import g
from neo4j.v1 import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

import os
import sys

uri = "bolt://{}:7687".format(os.getenv("NEO4J_HOST", "localhost"))

try:
    driver = GraphDatabase.driver(uri,
                                  auth=(os.getenv('NEO4J_USER', "neo4j"),
                                        os.getenv('NEO4J_PASSWORD', "bluetab")))
except ServiceUnavailable:
    print("Cannot access to neo4j database uri: {}".format(uri))
    sys.exit(0)

def get_db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session()
    return g.neo4j_db
