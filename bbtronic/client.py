import json
from typing import List

import requests

from bbtronic.types import BitbucketPage, PullRequest, PullRequestMergeStatus, BitbucketCompositeError


class BitbucketClient:
    base_uri: str
    _session: requests.Session

    def __init__(self, base_uri: str, access_token: str) -> None:
        super().__init__()
        self.base_uri = base_uri
        self.access_token = access_token
        self._session = requests.Session()
        self._session.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Atlassian-Token": "no-check",
            "Accept": "application/json",
            "Content": "application/json"
        }

    def list_pull_requests(self, project_key: str, repository_slug: str, state: str = "OPEN") -> List[PullRequest]:
        start = 0
        is_last_page = False
        values: List[PullRequest] = []
        while not is_last_page:
            r = self._session.get(
                f"{self.base_uri}/projects/{project_key}/repos/{repository_slug}/pull-requests",
                params={
                    "start": start,
                    "state": state
                }
            )
            j = json.loads(r.text)
            BitbucketCompositeError.check(j)
            page = BitbucketPage.from_json(value_from_json=PullRequest.from_json, **j)
            values.extend(page.values)
            start = page.next_page_start
            is_last_page = page.is_last_page
        return values

    def get_pull_requests(self, project_key: str, repository_slug: str, pull_request_id: int) -> PullRequest:
        r = self._session.get(
            f"{self.base_uri}/projects/{project_key}/repos/{repository_slug}/pull-requests/{pull_request_id}",
        )
        j = json.loads(r.text)
        BitbucketCompositeError.check(j)
        pr = PullRequest.from_json(**j)
        return pr

    def can_merge_pull_request(self, project_key: str, repository_slug: str, pull_request_id: int):
        r = self._session.get(
            f"{self.base_uri}/projects/{project_key}/repos/{repository_slug}/pull-requests/{pull_request_id}/merge",
        )
        j = json.loads(r.text)
        BitbucketCompositeError.check(j)
        return PullRequestMergeStatus.from_json(**j)

    def merge_pull_request(
            self, project_key: str, repository_slug: str, pull_request_id: int, pull_request_version: int
    ):
        r = self._session.post(
            f"{self.base_uri}/projects/{project_key}/repos/{repository_slug}/pull-requests/{pull_request_id}/merge",
            params={
                "version": pull_request_version
            },
        )
        j = json.loads(r.text)
        BitbucketCompositeError.check(j)
        return PullRequest.from_json(**j)

    def close(self):
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
