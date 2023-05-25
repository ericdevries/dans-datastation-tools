import requests

from datastation.common.utils import print_dry_run_message


class DataverseApi:

    def __init__(self, server_url, api_token):
        self.server_url = server_url
        self.api_token = api_token

    def get_contents(self, dry_run=False):
        headers = {'X-Dataverse-key': self.api_token}
        url = f'{self.server_url}/api/dataverses/root/contents'
    
        if dry_run:
            print_dry_run_message(method='GET', url=url, headers=headers)
            return None
        
        dv_resp = requests.get(url, headers=headers)
        dv_resp.raise_for_status()

        resp_data = dv_resp.json()['data']
        return resp_data

    