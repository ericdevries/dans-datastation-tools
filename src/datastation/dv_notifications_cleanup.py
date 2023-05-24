import argparse
import logging
import logging
from datetime import timedelta

from datastation.common.config import init
from datastation.common.utils import add_dry_run_arg
from datastation.dataverse.dataverse_client import DataverseClient
from datastation.dataverse.notifications import Notifications


def main():
    config = init()
    parser = argparse.ArgumentParser(description="Clean up old notifications")
    parser.add_argument(
        "--days-old",
        help="Minimum amount of days old",
        type=positive_int,
        required=True,
    )
    add_dry_run_arg(parser)
    args = parser.parse_args()

    dataverse_client = DataverseClient(config['dataverse'])

    notifications = Notifications(
        dataverse_client, 
        dry_run=args.dry_run
    )
    
    notifications.cleanup(args.days_old)


def positive_int(value):
    ivalue = int(value)

    if ivalue <= 0:
        raise argparse.ArgumentTypeError("value must be a number greater than zero")

    return ivalue


if __name__ == "__main__":
    main()
