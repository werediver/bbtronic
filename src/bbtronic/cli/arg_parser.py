from __future__ import annotations

from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum
from typing import Union


def parse_args() -> RunConfig:
    return RunConfig(**_mk_arg_parser().parse_args().__dict__)


def _mk_arg_parser() -> ArgumentParser:
    p = ArgumentParser()
    sps = p.add_subparsers()
    _configure_repo_cmd_parser(sps.add_parser(Command.LIST.value)).set_defaults(command=Command.LIST)
    _configure_pr_cmd_parser(sps.add_parser(Command.CHECK.value)).set_defaults(command=Command.CHECK)
    _configure_pr_cmd_parser(sps.add_parser(Command.MERGE.value)).set_defaults(command=Command.MERGE)
    _configure_pr_cmd_parser(sps.add_parser(Command.AUTOMERGE.value)).set_defaults(command=Command.AUTOMERGE)
    return p


def _configure_repo_cmd_parser(p: ArgumentParser) -> ArgumentParser:
    p.add_argument("path", type=RepositoryPath.parse, help=RepositoryPath.REF_REPR)
    return p


def _configure_pr_cmd_parser(p: ArgumentParser) -> ArgumentParser:
    p.add_argument("path", type=PullRequestPath.parse, help=PullRequestPath.REF_REPR)
    return p


class Command(Enum):
    LIST = "list"
    CHECK = "check"
    MERGE = "merge"
    AUTOMERGE = "automerge"


@dataclass
class RunConfig:
    command: Command
    path: Union[RepositoryPath, PullRequestPath]


@dataclass
class RepositoryPath:
    server_alias: str
    project_key: str
    repository_slug: str

    REF_REPR = "server_alias/project_key/repository_slug"

    @classmethod
    def parse(cls, s: str):
        try:
            return RepositoryPath(*s.split("/"))
        except TypeError:
            raise Exception(
                f"Cannot construct {RepositoryPath.__name__} from \"{s}\" "
                f"(expected a string of form \"{cls.REF_REPR}\")"
            )


@dataclass
class PullRequestPath(RepositoryPath):
    pull_request_id: int

    REF_REPR = "server_alias/project_key/repository_slug/pull_request_id"

    @classmethod
    def parse(cls, s: str):
        try:
            return PullRequestPath(*s.split("/"))
        except TypeError:
            raise Exception(
                f"Cannot construct {PullRequestPath.__name__} from \"{s}\" "
                f"(expected a string of form \"{cls.REF_REPR}\")"
            )
