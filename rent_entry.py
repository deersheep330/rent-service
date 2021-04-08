from rent.db.operations import create_engine_from_url, create_all_tables_from_orm
from rent.line_notify import send_message
from rent.utilities import get_db_connection_url
from rent.parser import RentParser
import sys

if __name__ == '__main__':

    is_first_time = False
    if len(sys.argv) == 2 and sys.argv[1] == 'init':
        is_first_time = True

    # init database
    engine = create_engine_from_url(get_db_connection_url())
    create_all_tables_from_orm(engine)

    # parse website and find new items for flat
    flat_parser = RentParser(is_first_time=is_first_time)
    flat_parser.parse()
    new_items = flat_parser.get_new_items_url()
    print(new_items)

    # send notification
    for new_item in new_items:
        send_message(new_item)
