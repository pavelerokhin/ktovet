from src.dsl.decorators import with_context
from src.etc.db import create, delete, execute, execute_get_results


@with_context
def create_db(db_name, schema):
    create(db_name=db_name, schema=schema)


@with_context
def delete_db(db_name):
    delete(db_name=db_name)


@with_context
def execute_query(db, query):
    execute(db=db, query=query)


@with_context
def execute_query_results(db, query):
    return execute_get_results(db=db, query=query)
