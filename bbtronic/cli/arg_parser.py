from argparse import ArgumentParser, Namespace
from typing import Callable


def mk_arg_parser() -> ArgumentParser:
    p = ArgumentParser()
    sps = p.add_subparsers()
    _configure_repo_cmd_parser(sps.add_parser("list")).set_defaults(command="list")
    _configure_pr_cmd_parser(sps.add_parser("check")).set_defaults(command="check")
    _configure_pr_cmd_parser(sps.add_parser("merge")).set_defaults(command="merge")
    _configure_pr_cmd_parser(sps.add_parser("automerge")).set_defaults(command="automerge")
    return p


def _configure_repo_cmd_parser(p: ArgumentParser) -> ArgumentParser:
    p.add_argument("path", help="server_name/project_key/repository_slug")
    return p


def _configure_pr_cmd_parser(p: ArgumentParser) -> ArgumentParser:
    p.add_argument("path", help="server_name/project_key/repository_slug/pull_request_id")
    return p
