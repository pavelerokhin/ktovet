from src.dsl.decorators import sln, function_with_result
from src.etc.db import create, delete, execute, execute_get_results


@sln
def create_db(db_name, schema):
    create(db_name=db_name, schema=schema)


@sln
def delete_db(db_name):
    delete(db_name=db_name)


@sln
def execute_query(db, query):
    execute(db=db, query=query)


@function_with_result
def execute_query_results(db, query):
    return execute_get_results(db=db, query=query)
