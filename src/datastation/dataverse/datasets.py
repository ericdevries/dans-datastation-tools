import json
from typing import Optional

from datastation.dataverse.dataverse_client import DataverseClient


class Datasets:
    def __init__(self, dataverse_client: DataverseClient, dry_run: bool = False):
        self.dataverse_client = dataverse_client
        self.dry_run = dry_run

    def print_dataset_attributes(self, storage: bool, role: str, pid: str):
        def process_dataset_attributes(
            dataset: dict,
            storage: bool,
            role: str,
        ):
            pid = (
                dataset["global_id"]
                if "global_id" in dataset
                else dataset["datasetPersistentId"]
            )

            attributes = {"pid": pid}

            if storage:
                dataset_with_files = dataset

                if "files" not in dataset_with_files:
                    dataset_with_files = self.dataverse_client.dataset(pid).get(
                        dry_run=self.dry_run
                    )

                if dataset_with_files:
                    attributes["storage"] = sum(
                        f["dataFile"]["filesize"] for f in dataset_with_files["files"]
                    )
                else:
                    raise Exception("Dataset not found")

            if role is not None:
                role_assignments = self.dataverse_client.dataset(
                    pid
                ).get_role_assignments(dry_run=self.dry_run)

                if role_assignments is not None:
                    attributes["users"] = [
                        user["assignee"].replace("@", "")
                        for user in role_assignments
                        if user["_roleAlias"] == role
                    ]

            print(json.dumps(attributes, indent=2))

        if pid is not None:
            dataset = self.dataverse_client.dataset(pid).get(dry_run=self.dry_run)

            if dataset:
                process_dataset_attributes(dataset, storage, role)
            else:
                raise Exception("Dataset not found")

            return

        contents = self.dataverse_client.dataverse().search(dry_run=self.dry_run)

        for result in contents:
            process_dataset_attributes(result, storage, role)
