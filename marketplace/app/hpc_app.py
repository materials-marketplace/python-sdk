"""This module contains all functionality interacting with hpc apps.
"""
import ast

from marketplace.app.utils import check_capability_availability
from marketplace.core import MarketPlaceClient


class HPPApp(MarketPlaceClient):
    """General HPC gateway app with all the supported capabilities."""

    @check_capability_availability("updateDataset")
    def upload(self, resourceid, source_path=str):
        """upload file to remote path `resourceid` from source path"""
        with open(source_path, "rb") as fh:
            self.put(
                path="updateDataset",
                params={"resourceid": f"{resourceid}"},
                files={"file": fh},
            )

    @check_capability_availability("getDataset")
    def download(self, resourceid, filename) -> str:
        """download file from `resourceid`
        return str of content"""
        resp = self.get(
            path="getDataset",
            params={"resourceid": f"{resourceid}"},
            json={"filename": filename},
        )

        return resp.text

    @check_capability_availability("deleteDataset")
    def delete(self, resourceid, filename):
        resp = self.delete(
            path="deleteDataset",
            params={"resourceid": f"{resourceid}"},
            json={"filename": filename},
        )
        return resp.text

    @check_capability_availability("newTransformation")
    def new_job(self, config=None):
        """Create a new job

        Actually it will create a new folder in specific user path on HPC
        Return the folder name for further opreration."""
        resp = self.post(path="newTransformation", json=config).text
        resp = ast.literal_eval(resp)

        return resp["resourceid"]

    @check_capability_availability("getTranspormationList")
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

    @check_capability_availability("stopTransformation")
    def cancel_job(self, resourceid):
        """cancel a job"""
        resp = self.post(
            path="stopTransformation", params={"resourceid": f"{resourceid}"}
        )

        return resp.text

    @check_capability_availability("deleteTransformation")
    def delete_job(self, resourceid):
        """delete job corresponded to path `resourceid`
        It actually drop entity from DB.
        """
        resp = self.delete(
            path="deleteTransformation", params={"resourceid": f"{resourceid}"}
        )

        return resp.text
