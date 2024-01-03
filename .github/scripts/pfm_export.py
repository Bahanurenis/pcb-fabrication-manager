import os
from string import Template
import requests
from dotenv import load_dotenv, dotenv_values

token = dotenv_values(".env").get("github_token")
headers = {"Authorization": f"Bearer {token}"}
GITHUB_URL = "https://api.github.com/graphql"
pfm_token = os.environ["PFM_TOKEN"]
issue_id = os.environ["ISSUE_ID"]
issue_body = os.environ["ISSUE_BODY"]


def _run_query(query: str, variables: dict = {}) -> dict:
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


def _find_issue():
    query = """
    query($owner:String!, $name:String!){
        repository(owner:$owner, name:$name){
            issues(first:10, labels:"pfm"){
                nodes{
                    id
                    body
                }
            }
        }
    }
    """
    variables = {
        "owner": "Bahanurenis",
        "name": "pcb-fabrication-manager",
    }
    response = _run_query(query=query, variables=variables)
    print(response)
    return response


def _delete_issue(issueId: str):
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
    response = _run_query(query=mutation, variables=variables)
    print(response)
    return response


if __name__ == "__main__":
    print(issue_id)
    print(issue_body)
    _find_issue()
    # _delete_issue("I_kwDOK18lRc57CSmc")
