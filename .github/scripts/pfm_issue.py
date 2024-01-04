from typing import List


class Issue:
    def __init__(self, data: dict):
        self._issue: dict = data

    @property
    def id(self) -> str:
        return self._issue["node_id"]

    @property
    def owner(self) -> str:
        return self._issue["user"]["login"]

    @property
    def body(self) -> str:
        return self._issue["body"]

    @property
    def labels(self) -> List[dict]:
        return self._issue["labels"]
