import argparse

from datastation.config import init
from typing import List, Optional
import logging
import sys
import json

from src.datastation.dv_api import (
    get_dataverse_contents,
    get_dataset,
    get_dataset_by_internal_id,
    get_dataset_roleassigments,
)

# TODO this should be somewhere else
class DataverseAPI:
    def __init__(self, server_url, api_token):
        self.server_url = server_url
        self.api_token = api_token

    def get_dataset_ids(self) -> List[int]:
        contents = get_dataverse_contents(self.server_url, self.api_token)
        result = []

        for content in contents:
            if content["type"] == "dataset":
                result.append(content["id"])

        return result

    def get_dataset(self, pid: str, version=":latest"):
        return get_dataset(self.server_url, self.api_token, pid, version)

    def get_dataset_by_internal_id(self, id: int, version=":latest"):
        return get_dataset_by_internal_id(self.server_url, self.api_token, id, version)

    def get_dataset_roleassignments(self, pid: str):
        return get_dataset_roleassigments(self.server_url, self.api_token, pid)


class AttributeOptions:
    user_role: Optional[str] = None
    storage: bool = False


def main():
    config = init()

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

    args = parser.parse_args()

    options = AttributeOptions()
    options.storage = args.storage
    options.user_role = args.user_with_role

    server_url = config["dataverse"]["server_url"]
    api_token = config["dataverse"]["api_token"]
    dataverse_api = DataverseAPI(server_url=server_url, api_token=api_token)

    output = []

    try:
        datasets = get_dataset_list(dataverse_api, pid=args.pid)

        for dataset in datasets:
            result = get_dataset_attributes(dataverse_api, dataset, options)
            output.append(result)

    except Exception as e:
        logging.error("Error while retrieving dataset attributes: %s", e)

    # if no datasets were found but a specific ID was provided, log an error
    if not args.all_datasets and len(output) < 1:
        logging.error("Dataset with pid %s not found", args.pid)
        sys.exit(1)

    print_output(output, args)


def get_dataset_list(dataverse_api: DataverseAPI, pid: Optional[str]):
    if pid is not None:
        dataset = dataverse_api.get_dataset(pid)
        return [dataset]

    dataset_ids = dataverse_api.get_dataset_ids()
    result = []

    for dataset_id in dataset_ids:
        dataset = dataverse_api.get_dataset_by_internal_id(dataset_id)
        result.append(dataset)

    return result


def get_dataset_attributes(
    dataverse_api: DataverseAPI, dataset: dict, options: AttributeOptions
):
    pid = dataset["datasetPersistentId"]
    attributes = {"pid": pid}

    if options.storage:
        attributes["storage"] = sum(f["dataFile"]["filesize"] for f in dataset["files"])

    if options.user_role is not None:
        role_assignments = dataverse_api.get_dataset_roleassignments(pid)
        attributes["users"] = [
            user["assignee"].replace("@", "")
            for user in role_assignments
            if user["_roleAlias"] == options.user_role
        ]

    return attributes


def print_output(output: List[dict], args: argparse.Namespace):
    if not args.all_datasets:
        print_json(output[0])
    else:
        print_json(output)


def print_json(output):
    print(json.dumps(output, indent=2))
