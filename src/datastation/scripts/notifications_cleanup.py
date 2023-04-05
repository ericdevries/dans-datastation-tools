import argparse
import logging
import sys
import psycopg
import logging
from datetime import timedelta

from datastation.config import init


class DataverseDBConnection:
    def __init__(self, host, dbname, user, password):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password

    def __enter__(self):
        self.connection = psycopg.connect(
            "host={} dbname={} user={} password={}".format(
                self.host, self.dbname, self.user, self.password
            )
        )
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def cleanup_notifications(conn, days_old):
    logging.info("Cleaning up notifications older than %s days", days_old)

    notifications_older_than = timedelta(days=days_old)

    delete_statement = """
        delete
        from usernotification
        where senddate < now() - %s
    """

    with conn.cursor() as cursor:
        try:
            delete_result = cursor.execute(delete_statement, (notifications_older_than,))
            amount_deleted = delete_result.rowcount
            conn.commit()

            logging.info("Deleted %s notifications", amount_deleted)

        except psycopg.DatabaseError as error:
            logging.error(error)
            sys.exit(
                "FATAL ERROR: problem accessing database with {} ".format(
                    delete_statement
                )
            )


def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("value must be a number greater than zero")
    return ivalue


def main():
    config = init()
    parser = argparse.ArgumentParser(description="Clean up old notifications")
    parser.add_argument(
        "--days-old",
        help="Minimum amount of days old",
        type=positive_int,
        required=True,
    )
    args = parser.parse_args()

    dvndb_conn = DataverseDBConnection(
        config["dataverse"]["db"]["host"],
        config["dataverse"]["db"]["dbname"],
        config["dataverse"]["db"]["user"],
        config["dataverse"]["db"]["password"],
    )

    with dvndb_conn as conn:
        cleanup_notifications(conn, args.days_old)


if __name__ == "__main__":
    main()
