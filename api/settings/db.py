from flask import g
from neo4j.v1 import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from api.app import app

import sys


uri = "bolt://{}:{}".format(app.config["NEO4J_HOST"], app.config["NEO4J_PORT"])


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
            auth=(app.config["NEO4J_USER"],
                  app.config["NEO4J_PASSWORD"]))

    except ServiceUnavailable:
        print("Cannot access to neo4j database uri: {}".format(uri))
        sys.exit(0)

    return driver


def create_session(driver):
    return driver.session()
