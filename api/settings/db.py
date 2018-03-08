from flask import g
from neo4j.v1 import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

import os
import sys


uri = "bolt://{}:7687".format(os.getenv("NEO4J_HOST", "localhost"))


def get_neo4j_db():

    if not hasattr(g, "neo4j_driver") or g.neo4j_driver.closed():
        g.neo4j_driver = create_connection()

    if not hasattr(g, "neo4j_session") or g.neo4j_session.closed():
        g.neo4j_session = create_session(g.neo4j_driver)

    return g.neo4j_session


def create_connection():

    try:
        driver = GraphDatabase.driver(
            uri,
            auth=(os.getenv("NEO4J_USER", "neo4j"),
                  os.getenv("NEO4J_PASSWORD", "bluetab")))

    except ServiceUnavailable:
        print("Cannot access to neo4j database uri: {}".format(uri))
        sys.exit(0)

    return driver


def create_session(driver):
    return driver.session()
