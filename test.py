from datetime import datetime, timedelta

from rent.db import create_engine_from_url, create_all_tables_from_orm, delete_older_than, start_session, insert, count
from rent.models import House
from rent.parser import RentParser
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


def test_parsing_website():
    flat_parser = RentParser(rent_type='flat')
    flat_parser.parse()
    new_items = flat_parser.new_items
    delete_older_than(session, House, House.date, datetime.now().date())
    session.commit()
    assert len(new_items) > 0
