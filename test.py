from datetime import datetime, timedelta

from rent.db import create_engine_from_url, create_all_tables_from_orm, delete_older_than, start_session, insert, count
from rent.models import House
from rent.utilities import get_db_connection_url

if __name__ == '__main__':

    # init database
    engine = create_engine_from_url(get_db_connection_url())
    session = start_session(engine)
    create_all_tables_from_orm(engine)

    insert(session, House, {
        'id': 'test1',
        'date': datetime(1970, 1, 1)
    })
    insert(session, House, {
        'id': 'test2',
        'date': datetime(1970, 1, 1)
    })
    session.commit()

    total = count(session, House)
    print(total)

    count = delete_older_than(session, House, House.date, datetime.now().date() - timedelta(days=60))
    print(count)
    session.commit()

