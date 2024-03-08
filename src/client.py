from keboola.component import UserException
from keboola.http_client import HttpClient
from requests.exceptions import HTTPError

BASE_URL = 'https://api.portable.io/v2/'


class PortableClient(HttpClient):

    def __init__(self, token):
        super().__init__(BASE_URL)
        self.update_auth_header({"Authorization": f'Bearer {token}'})

    def list_connectors(self) -> dict:
        """
        List all flows
        """

        try:
            response = self.get("connectors")
        except HTTPError as e:
            raise UserException(f"Error while listing flows: {e}")

        return response.get("data", [])

    def list_flows(self) -> dict:
        """
        List all flows
        """

        try:
            response = self.get("flows")
        except HTTPError as e:
            raise UserException(f"Error while listing flows: {e}")

        return response.get("data", [])

    def run_flow(self, flow_id: str) -> dict:
        """
        List all flows
        """

        try:
            response = self.post(f"flows/{flow_id}/run")
        except HTTPError as e:
            raise UserException(f"Error while listing flows: {e}")

        return response['message']

    def get_flow_status(self, flow_id: str) -> dict:
        """
        List all flows
        """

        try:
            response = self.get(f"flows/{flow_id}/status")
        except HTTPError as e:
            raise UserException(f"Error while listing flows: {e}")

        return response
