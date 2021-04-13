from rent.db.operations import create_engine_from_url, create_all_tables_from_orm
from rent.line_notify import send_message
from rent.utilities import get_db_connection_url
from rent.parser import SaleParser

if __name__ == '__main__':

    # init database
    engine = create_engine_from_url(get_db_connection_url())
    create_all_tables_from_orm(engine)

    # parse website and find new items for flat
    parser = SaleParser()
    parser.parse()
    new_items = parser.get_new_items_url()
    print(new_items)

    # send notification
    content = ''
    for index, new_item in enumerate(new_items, start=1):
        content += f'\n【{index}】 {new_item}\n'
    if content != '':
        send_message(content)
