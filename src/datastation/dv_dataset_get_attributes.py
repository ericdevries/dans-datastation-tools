import argparse

from datastation.common.config import init
from typing import List, Optional
import logging
import sys
import json

from datastation.dataverse.dataverse_client import DataverseClient
from datastation.common.utils import add_dry_run_arg


class AttributeOptions:
    user_role: Optional[str] = None
    storage: bool = False


def main():
    config = init()
    dataverse = DataverseClient(config["dataverse"])

    parser = argparse.ArgumentParser(description="Retrieves attributes of a dataset")

    parser.add_argument(
        "--user-with-role",
        dest="user_with_role",
        help="List users with a specific role on the dataset",
    )
    parser.add_argument(
        "--storage",
        dest="storage",
        action="store_true",
        help="The storage in bytes",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("pid", help="The dataset pid", nargs="?")
    group.add_argument(
        "--all",
        dest="all_datasets",
        action="store_true",
        help="All datasets in the dataverse",
        required=False,
    )

    add_dry_run_arg(parser)

    args = parser.parse_args()

    get_dataset_attributes(args, dataverse)


def get_dataset_attributes(args, dataverse: DataverseClient):
    options = AttributeOptions()
    options.storage = args.storage
    options.user_role = args.user_with_role

    try:
        datasets = get_dataset_list(dataverse, pid=args.pid, dry_run=args.dry_run)

        for dataset in datasets:
            result = process_dataset_attributes(dataverse, dataset, options)
            print_output(result)

    except Exception as e:
        logging.error("Error while retrieving dataset attributes: %s", e)


def get_dataset_list(
    dataverse: DataverseClient, pid: Optional[str], dry_run=False
) -> List[dict]:
    if pid is not None:
        dataset = dataverse.dataset(pid).get(dry_run=dry_run)
        return [dataset] if dataset is not None else []

    contents = dataverse.dataverse().get_contents(dry_run=dry_run)
    result = []

    if contents is not None:
        for content in contents:
            if content["type"] == "dataset":
                doi = f'{content["protocol"]}:{content["authority"]}/{content["identifier"]}'
                dataset = dataverse.dataset(doi).get(dry_run=dry_run)

                if dataset is not None:
                    result.append(dataset)

    return result


def process_dataset_attributes(
    dataverse: DataverseClient, dataset: dict, options: AttributeOptions, dry_run=False
):
    pid = dataset["datasetPersistentId"]
    attributes = {"pid": pid}

    if options.storage:
        attributes["storage"] = sum(f["dataFile"]["filesize"] for f in dataset["files"])

    if options.user_role is not None:
        role_assignments = dataverse.dataset(pid).get_role_assignments(dry_run=dry_run)

        if role_assignments is not None:
            attributes["users"] = [
                user["assignee"].replace("@", "")
                for user in role_assignments
                if user["_roleAlias"] == options.user_role
            ]

    return attributes


def print_output(output: dict):
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
