from rent.db.operations import create_engine_from_url, create_all_tables_from_orm
from rent.line_notify import send_message
from rent.utilities import get_db_connection_url
from rent.parser import RentParser

if __name__ == '__main__':

    # init database
    engine = create_engine_from_url(get_db_connection_url())
    create_all_tables_from_orm(engine)

    # parse website and find new items for suite
    suite_parser = RentParser(rent_type='suite')
    suite_parser.parse()
    new_items = suite_parser.get_new_items_url()
    print(new_items)

    # send notification
    for new_item in new_items:
        send_message(new_item)

    # parse website and find new items for flat
    flat_parser = RentParser(rent_type='flat')
    flat_parser.parse()
    new_items = flat_parser.get_new_items_url()
    print(new_items)

    # send notification
    for new_item in new_items:
        send_message(new_item)
