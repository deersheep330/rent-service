from datetime import datetime, timedelta

from rent.db import create_engine_from_url, create_all_tables_from_orm, delete_older_than, start_session, insert, count
from rent.models import House
from rent.parser import RentParser, SaleParser
from rent.utilities import get_db_connection_url

engine = create_engine_from_url(get_db_connection_url())
session = start_session(engine)


def test_create_tables():
    create_all_tables_from_orm(engine)


def test_insert():
    insert(session, House, {'id': 'test1', 'date': datetime(1970, 1, 1)})
    insert(session, House, {'id': 'test2', 'date': datetime(1970, 1, 1)})
    session.commit()

    total = count(session, House)
    assert total == 2


def test_delete_old_records():
    count = delete_older_than(session, House, House.date, datetime.now().date() - timedelta(days=60))
    session.commit()
    assert count == 2


def test_rent_parsing():

    count = delete_older_than(session, House, House.date, datetime.now().date())
    print(f'delete {count} old records')
    session.commit()

    flat_parser = RentParser()
    flat_parser.parse()
    new_items = flat_parser.new_items
    assert len(new_items) > 0


def test_sale_parsing():

    count = delete_older_than(session, House, House.date, datetime.now().date())
    print(f'delete {count} old records')
    session.commit()

    retry = 0
    max_retry = 5
    new_items_len = 0
    while new_items_len == 0 and retry < max_retry:
        parser = SaleParser()
        parser.parse()
        new_items = parser.new_items
        new_items_len = len(new_items)
        retry += 1
    assert len(new_items_len) > 0
