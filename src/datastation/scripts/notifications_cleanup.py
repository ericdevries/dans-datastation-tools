import argparse
import logging
import sys
import psycopg
import logging
from datetime import timedelta

from datastation.config import init


def cleanup_notifications(dvndb_conn, days_old):
    notifications_older_than = timedelta(days=days_old)
    logging.info("Cleaning up notifications older than %s days", days_old)

    delete_statement = """
        delete
        from usernotification
        where senddate < now() - %s
    """
    
    with dvndb_conn.cursor() as dvndb_cursor:
        try:
            result = dvndb_cursor.execute(delete_statement, (notifications_older_than,))
            amount_deleted = result.rowcount
            dvndb_conn.commit()

            logging.info("Deleted %s notifications", amount_deleted)
            
        except psycopg.DatabaseError as error:
            logging.error(error)
            sys.exit("FATAL ERROR: problem accessing database with {} ".format(delete_statement))


def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("value must be a number greater than zero")
    return ivalue

def main():
    config = init()
    parser = argparse.ArgumentParser(description='Clean up old notifications')
    parser.add_argument("--days-old", help="Minimum amount of days old", type=positive_int, required=True)
    args = parser.parse_args()

    dvndb_conn = None

    try:
        dvndb_conn = connect_to_database(config['dataverse']['db']['host'], config['dataverse']['db']['dbname'],
                                         config['dataverse']['db']['user'], config['dataverse']['db']['password'])
        cleanup_notifications(dvndb_conn, args.days_old)
    except psycopg.DatabaseError as error:
        logging.error(error)
        sys.exit("FATAL ERROR: No connection with database established: {}".format(error))
    finally:
        if dvndb_conn is not None:
            dvndb_conn.close()


def connect_to_database(host, dbname, user: str, password: str):
    return psycopg.connect(
        "host={} dbname={} user={} password={}".format(host, dbname, user, password))


if __name__ == '__main__':
    main()
