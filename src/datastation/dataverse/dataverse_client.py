from datastation.common.database import Database
from datastation.dataverse.banner_api import BannerApi
from datastation.dataverse.builtin_users import BuiltInUsersApi
from datastation.dataverse.file_api import FileApi
from datastation.dataverse.dataset_api import DatasetApi


class DataverseClient:
    """ A client for the Dataverse API. """

    def __init__(self, config: dict):
        self.server_url = config['server_url']
        self.api_token = config['api_token']
        self.unblock_key = config['unblock_key'] if 'unblock_key' in config else None
        self.safety_latch = config['safety_latch']
        self.db_config = config['db']

    def banner(self):
        return BannerApi(self.server_url, self.api_token, self.unblock_key)

    def dataset(self, pid):
        return DatasetApi(pid, self.server_url, self.api_token, self.unblock_key, self.safety_latch)

    def file(self, id):
        return FileApi(id, self.server_url, self.api_token, self.unblock_key, self.safety_latch)

    def built_in_users(self, builtin_users_key):
        return BuiltInUsersApi(self.server_url, self.api_token, builtin_users_key, self.unblock_key)

    def database(self):
        return Database(self.db_config)
