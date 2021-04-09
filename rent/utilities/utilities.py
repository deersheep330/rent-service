import os


def read_env(var):
    res = os.getenv(var)
    if res is None:
        raise Exception(f'Cannot get {var} from env')
    else:
        print(f'{var}: {res}')
        return res


def get_db_connection_url():
    return read_env('DB_CONNECTION_URL')


def get_line_token():
    return read_env('LINE_TOKEN')


def get_line_token_of_yu():
    return read_env('YU_LINE_TOKEN')
