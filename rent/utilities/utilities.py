import os
from configparser import ConfigParser


def read_variable_from_config(var):
    config = ConfigParser()
    config.read_file(open('variables.ini'))
    res = config['DEFAULT'][var]
    if res is None:
        raise Exception(f'Cannot get {var} from ini file')
    else:
        print(f'{var}: {res}')
        return res


def read_variable_from_env(var):
    res = os.getenv(var)
    if res is None:
        raise Exception(f'Cannot get {var} from env')
    else:
        print(f'{var}: {res}')
        return res


def get_variable(var):

    print(f'try to get {var} ...')

    try:
        return read_variable_from_config(var)
    except Exception as e:
        print(e)

    try:
        return read_variable_from_env(var)
    except Exception as e:
        print(e)

    raise Exception(f'{var} not found')


def get_db_connection_url():
    return get_variable('DB_CONNECTION_URL')


def get_line_token():
    return get_variable('LINE_TOKEN')
