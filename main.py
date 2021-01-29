from rent.db.operations import create_engine_from_url, start_session, create_all_tables_from_orm


if __name__  == '__main__':
    engine = create_engine_from_url('root:admin@localhost:3306/mydb')
    create_all_tables_from_orm(engine)
