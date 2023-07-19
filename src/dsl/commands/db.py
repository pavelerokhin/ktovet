from src.dsl.decorators import function, function_with_result
from src.etc.db import create, delete, execute


@function
def create_db(db_name, schema):
    create(db_name=db_name, schema=schema)


@function
def delete_db(db_name):
    delete(db_name=db_name)


@function
def execute_query(db_name, query):
    execute(db_name=db_name, query=query)

@function_with_result
def execute_query(db_name, query):
    execute(db_name=db_name, query=query)