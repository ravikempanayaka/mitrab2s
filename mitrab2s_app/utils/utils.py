import logging
from django.db import connection, utils

LOGGER = logging.getLogger(__name__)


def dict_fetchall(cursor):
    """
    Return all rows from a cursor as a dict
    :param cursor:
    :return dict of sql query results:
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def execute_query_return_query_result(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        try:
            result = dict_fetchall(cursor)
            return result
        except Exception as f:
            LOGGER.debug('No dict fetchall : ' + str(f))
    except utils.ConnectionHandler as ch:
        LOGGER.error("ConnectionHandler : " + str(ch))
        raise Exception("ConnectionHandler : " + str(ch))
    except utils.DatabaseError as idn:
        LOGGER.error("DatabaseError : " + str(idn))
        raise Exception("DatabaseError : " + str(idn))
    except Exception as e:
        LOGGER.error("Exception error: " + str(e))
        raise Exception("Exception error: " + str(e))
