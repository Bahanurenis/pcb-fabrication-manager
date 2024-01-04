import json
import os
import re
from io import StringIO
from string import Template
from typing import List
import requests
import yaml
import pandas as pd
from pathlib import Path
from pfm_issue import Issue
from config import Config
from csv_handler import PfmCsvHandler


pfm_token = os.environ.get("PFM_AUTH")
issue_payload: dict = json.loads(os.environ["ISSUE"])
outputh_path: str = os.environ["WORKSPACE_PATH"]
headers = {"Authorization": f"Bearer {pfm_token}"}
GITHUB_URL = "https://api.github.com/graphql"


class PfmGitHub:
    def __init__(self):
        self._issue = Issue(data=issue_payload)
        self._config_content = None
        self._csv_content = None
        self._validate_issue(self._issue)

    def _validate_issue(self, issue: Issue) -> bool:
        _labels: List[dict] = issue.labels
        _pfm_label = ""
        for label in _labels:
            if label["name"] == "pfm":
                _pfm_label = "pfm"
                break
        if _pfm_label != "pfm":
            print(
                "ATTENTION: If the issue has sensitive data please delete your issue, and create another one with pfm label or use the template"
            )
            raise Exception(
                "issue should have pfm label, workflow will not run. If you create this issue to build a new CSV please be carefull because issue will not be deleted\n"
            )

        _res_config_url = re.search(
            "(?P<url>https?://github.com/[^\s]+/config.txt)", issue.body
        )
        _res_csv_url = re.search(
            "(?P<url>https?://github.com/[^\s]+/input.csv)", issue.body
        )
        if _res_config_url == None:
            self._delete_issue(issue.id)
            raise Exception(
                "The pfm issue should have config.txt, PFM is deleting your issue..."
            )

        elif _res_csv_url == None:
            self._delete_issue(issue.id)
            raise Exception(
                "The pfm issue should have input.csv,PFM is deleting your issue..."
            )
        else:
            print("PROCESS IS STARTING")
            config_response = requests.get(_res_config_url.group(0), headers=headers)
            csv_response = requests.get(_res_csv_url.group(0), headers=headers)
            if config_response.status_code == 200 and csv_response.status_code == 200:
                self._config_content = config_response.content
                self._csv_content = csv_response.text
            else:
                self._delete_issue(issue.id)
                raise Exception(
                    "Pfm couldn't get the content from GitHub, your issue will be deleted. Process is stopping. Create a bug issue"
                )
        print(
            "Issue was created successfully. Now your issue will be deleted to protect your data"
        )
        self._delete_issue(issue.id)

    def build_csv_with_GH(self):
        if self._config_content == None or self._csv_content == None:
            print(
                "Informations are not correct, please create a new issue with proper data"
            )
            return
        # Create Config
        try:
            _config: dict = yaml.safe_load(self._config_content)
            self._config = Config(_config)
        except yaml.YAMLError as e:
            print(f"Config file couldn't be created: {e}")
            # TODO: remove if this return is meaningless
            return
        # create pandas.DataFrame for csv
        try:
            csv_string_io = StringIO(self._csv_content)
            self._df = pd.read_csv(csv_string_io, on_bad_lines="warn")
        except:
            print("Input data couldn't be read")
            return
        _csv_handler = PfmCsvHandler(config=self._config, dataFrame=self._df)
        # PATH
        _save_output_path: Path = Path(
            outputh_path + "/" + str(self._issue.id) + "_" + "output.csv"
        )
        print("PROCESS IS FINISHED\n")
        print(f"Output file will save in {_save_output_path}")
        _csv_handler.export_new_csv_data(output_csv_path=_save_output_path)

    def _run_query(self, query: str, variables: dict = {}) -> dict:
        response = requests.post(
            GITHUB_URL,
            json={"query": query, "variables": variables},
            headers=headers,
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Query failed to run by returning code of {response.status_code}, {query}"
            )

    def _delete_issue(self, issueId: str):
        mutation = """
        mutation DeleteIssue($id:ID!){
            deleteIssue(input:{issueId:$id}) {
                repository {
                    name
                }
            }
        }
        """
        variables = {"id": issueId}
        response = self._run_query(query=mutation, variables=variables)
        print(response)
        return response


if __name__ == "__main__":
    pfm_gh = PfmGitHub()
    print("BUILDING.....")
    pfm_gh.build_csv_with_GH()
