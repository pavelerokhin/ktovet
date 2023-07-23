from src.dsl.model.decorators import with_context
from src.etc.db import *


@with_context
def create_database(db_name, schema):
    create(db_name=db_name, schema=schema)


@with_context
def delete_database(db_name):
    delete(db_name=db_name)


@with_context
def execute_query(db, query):
    execute(db=db, query=query)


@with_context
def execute_query_results(db, query):
    return execute_get_results(db=db, query=query)


@with_context
def get_database(db_name):
    return get_db(db_name=db_name)


@with_context
def insert(db, query_template, context, values):
    to_insert = list(zip(*[context.get(key) for key in values]))
    for vv in to_insert:
        sql_query = query_template.replace("?", "%s")
        sql_query = sql_query % vv
        execute(db, sql_query)
    # Format the SQL query string with the provided lists
