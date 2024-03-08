"""
Template Component main class.

"""
import logging
import time

from keboola.component.base import ComponentBase, sync_action
from keboola.component.exceptions import UserException
from keboola.component.sync_actions import SelectElement

from configuration import Configuration
from client import PortableClient


class Component(ComponentBase):
    """
    """

    def __init__(self):
        self.cfg: Configuration
        self.client: PortableClient
        super().__init__()

    def _init_configuration(self) -> None:
        self.validate_configuration_parameters(Configuration.get_dataclass_required_parameters())
        self.cfg: Configuration = Configuration.load_from_dict(self.configuration.parameters)

    def _init_client(self) -> None:
        self.client = PortableClient(self.cfg.credentials.pswd_api_token)

    def run(self):
        """
        Main execution code
        """

        self._init_configuration()
        self._init_client()

        if not self.cfg.flow_id:
            raise UserException("Flow ID needs to be set to run the flow.")

        result = self.client.run_flow(self.cfg.flow_id)

        if result == "Created":
            logging.info("Flow run created")
        else:
            logging.warning(f"Flow run not created with status {result}")

        while self.cfg.wait_until_finished:

            status = self.client.get_flow_status(self.cfg.flow_id)
            if status['lifecycle'] == 'PENDING':
                logging.info("Flow is pending")
            elif status['lifecycle'] == 'RUNNING':
                logging.info("Flow is running")
            else:
                logging.info(f"Flow finished with status {status}")
                if self.cfg.fail_on_error:
                    if status['errors'] is not None:
                        raise UserException(f"Flow finished with error: {str(status['errors'])}")
                break

            time.sleep(10)

    @sync_action('list_flows')
    def list_flows(self):
        self._init_configuration()
        self._init_client()

        flows = self.client.list_flows()

        return [SelectElement(label=f"[{f['id']}] {f['displayName']}", value=f['id']) for f in flows]


"""
        Main entrypoint
"""
if __name__ == "__main__":
    try:
        comp = Component()
        # this triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
