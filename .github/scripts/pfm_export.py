import os
from string import Template
import requests
from dotenv import load_dotenv, dotenv_values

token = dotenv_values(".env").get("github_token")
headers = {"Authorization": f"Bearer {token}"}
GITHUB_URL = "https://api.github.com/graphql"


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
    # _find_issue()
    _delete_issue("I_kwDOK18lRc57CSmc")
