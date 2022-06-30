"""This module contains all functionality interacting with hpc apps.
"""
import ast
from urllib.parse import urljoin

from marketplace.app.utils import camel_to_snake, check_capability_availability
from marketplace.core import MarketPlaceClient


class HpcGatewayApp(MarketPlaceClient):
    """General HPC gateway app with all the supported capabilities."""

    def __init__(self, client_id, **kwargs):
        super().__init__(**kwargs)
        self.client_id = client_id
        # Must be run before the marketplace_host_url is updated to include the proxy.
        self.set_capabilities()
        self.marketplace_host_url = urljoin(
            self.marketplace_host_url, f"mp-api/proxy/{self.client_id}/"
        )

    def set_capabilities(self):
        """Query the platform to get the capabilities supported by a certain
        app."""
        app_service_path = f"application-service/applications/{self.client_id}"
        response = self.get(path=app_service_path).json()
        capability_info = response["capabilities"]
        self.capabilities = []
        for capability in capability_info:
            self.capabilities.append(camel_to_snake(capability["name"]))

    @check_capability_availability
    def heartbeat(self) -> str:
        """Check the heartbeat of the application.

        Returns:
            str: heartbeat
        """
        return self.get(path="heartbeat").text

    @check_capability_availability("update_dataset")
    def upload(self, resourceid, source_path=str):
        """upload file to remote path `resourceid` from source path"""
        with open(source_path, "rb") as fh:
            self.put(
                path="updateDataset",
                params={"resourceid": f"{resourceid}"},
                files={"file": fh},
            )

    @check_capability_availability("get_dataset")
    def download(self, resourceid, filename) -> str:
        """download file from `resourceid`
        return str of content"""
        resp = self.get(
            path="getDataset",
            params={"resourceid": f"{resourceid}"},
            json={"filename": filename},
        )

        return resp.text

    @check_capability_availability("delete_dataset")
    def delete(self, resourceid, filename):
        resp = self.delete(
            path="deleteDataset",
            params={"resourceid": f"{resourceid}"},
            json={"filename": filename},
        )
        return resp.text

    @check_capability_availability("new_transformation")
    def new_job(self, config=None):
        """Create a new job

        Actually it will create a new folder in specific user path on HPC
        Return the folder name for further opreration."""
        resp = self.post(path="newTransformation", json=config).text
        resp = ast.literal_eval(resp)

        return resp["resourceid"]

    @check_capability_availability("get_transpormationList")
    def list_job(self):
        """List the jobs"""
        return self.get(path="getTransformationList").json()

    @check_capability_availability("startTransformation")
    def run_job(self, resourceid):
        """submit job in the path `resourceid`
        It actually execute sbatch submit.sh in remote
        Need job script `submit.sh` uploaded to the folder
        TODO, check the job script ready"""
        resp = self.post(
            path="startTransformation", params={"resourceid": f"{resourceid}"}
        )

        return resp.text

    @check_capability_availability("stop_transformation")
    def cancel_job(self, resourceid):
        """cancel a job"""
        resp = self.post(
            path="stopTransformation", params={"resourceid": f"{resourceid}"}
        )

        return resp.text

    @check_capability_availability("delete_transformation")
    def delete_job(self, resourceid):
        """delete job corresponded to path `resourceid`
        It actually drop entity from DB.
        """
        resp = self.delete(
            path="deleteTransformation", params={"resourceid": f"{resourceid}"}
        )

        return resp.text
