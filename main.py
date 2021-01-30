from rent.db.operations import create_engine_from_url, create_all_tables_from_orm
from rent.utilities import get_db_connection_url
from rent.parser import RentParser

if __name__  == '__main__':
    #engine = create_engine_from_url(get_db_connection_url())
    #create_all_tables_from_orm(engine)
    rent_parser = RentParser()
    rent_parser.parse()
