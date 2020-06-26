import random
import time

import requests

from bbtronic.cli.arg_parser import Command, parse_args
from bbtronic.cli.config import load_config
from bbtronic.client import BitbucketClient
from bbtronic.types import BitbucketCompositeError

if __name__ == "__main__":
    run_config = parse_args()
    config = load_config()

    if run_config.command == Command.LIST:
        config_server = config.find_server(alias=run_config.path.server_alias)
        with BitbucketClient(
                base_uri=config_server.base_uri,
                access_token=config_server.access_token
        ) as client:
            prs = client.list_pull_requests(run_config.path.project_key, run_config.path.repository_slug)
            for pr in prs:
                print(f"#{pr.id} {pr.title}")
    elif run_config.command == Command.CHECK:
        config_server = config.find_server(alias=run_config.path.server_alias)
        with BitbucketClient(
                base_uri=config_server.base_uri,
                access_token=config_server.access_token
        ) as client:
            status = client.can_merge_pull_request(
                run_config.path.project_key, run_config.path.repository_slug, run_config.path.pull_request_id
            )
            print(status)
    elif run_config.command == Command.MERGE:
        config_server = config.find_server(alias=run_config.path.server_alias)
        with BitbucketClient(
                base_uri=config_server.base_uri,
                access_token=config_server.access_token
        ) as client:
            pr = client.get_pull_requests(
                run_config.path.project_key, run_config.path.repository_slug, run_config.path.pull_request_id
            )
            result = client.merge_pull_request(
                run_config.path.project_key, run_config.path.repository_slug, run_config.path.pull_request_id,
                pull_request_version=pr.version
            )
            print(result)
    elif run_config.command == Command.AUTOMERGE:
        config_server = config.find_server(alias=run_config.path.server_alias)
        with BitbucketClient(
                base_uri=config_server.base_uri,
                access_token=config_server.access_token
        ) as client:
            random.seed()
            base_delay = 5  # s
            variation = 0.2  # fraction
            while True:
                try:
                    status = client.can_merge_pull_request(
                        run_config.path.project_key, run_config.path.repository_slug, run_config.path.pull_request_id
                    )
                    print(status)
                    if status.can_merge:
                        pr = client.get_pull_requests(
                            run_config.path.project_key,
                            run_config.path.repository_slug,
                            run_config.path.pull_request_id
                        )
                        result = client.merge_pull_request(
                            run_config.path.project_key,
                            run_config.path.repository_slug,
                            run_config.path.pull_request_id,
                            pull_request_version=pr.version
                        )
                        print(result)
                        exit(0)
                except BitbucketCompositeError as e:
                    print(e)
                except requests.exceptions.ConnectionError as e:
                    # May happen when a keep-alive connection is closed by the server
                    # See https://github.com/psf/requests/issues/4664
                    print(e)
                delay = base_delay * random.uniform(1 - variation, 1 + variation)
                time.sleep(delay)
