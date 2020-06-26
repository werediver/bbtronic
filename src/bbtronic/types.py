from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar, Callable, List, Optional

T = TypeVar("T")
U = TypeVar("U")


@dataclass(frozen=True)
class BitbucketPage(Generic[T]):
    start: int
    size: int
    limit: int
    is_last_page: bool
    next_page_start: Optional[int]
    values: List[T]

    # noinspection PyPep8Naming
    @classmethod
    def from_json(
            cls, value_from_json: Callable[[any], U],
            start: int, size: int, limit: int, isLastPage: bool, values: List, nextPageStart: Optional[int] = None,
            *args, **kwargs
    ) -> BitbucketPage[U]:
        return cls(
            start=start,
            size=size,
            limit=limit,
            is_last_page=isLastPage,
            next_page_start=nextPageStart,
            values=[value_from_json(**value) for value in values]
        )


@dataclass(frozen=True)
class PullRequest:
    id: int
    version: int
    state: str
    open: bool
    closed: bool
    title: str

    # noinspection PyShadowingBuiltins
    @classmethod
    def from_json(
            cls,
            id: int, version: int, state: str, open: bool, closed: bool, title: str,
            *args, **kwargs
    ) -> PullRequest:
        return cls(id=id, version=version, state=state, open=open, closed=closed, title=title)


@dataclass(frozen=True)
class PullRequestMergeStatus:
    can_merge: bool
    conflicted: bool
    outcome: str
    vetoes: List[PullRequestMergeVeto]

    # noinspection PyPep8Naming
    @classmethod
    def from_json(
            cls,
            canMerge: bool, conflicted: bool, outcome: str, vetoes: List,
            *args, **kwargs
    ) -> PullRequestMergeStatus:
        return cls(
            can_merge=canMerge,
            conflicted=conflicted,
            outcome=outcome,
            vetoes=[PullRequestMergeVeto.from_json(**veto) for veto in vetoes]
        )


@dataclass(frozen=True)
class PullRequestMergeVeto:
    summary_message: str
    detailed_message: str

    # noinspection PyPep8Naming
    @classmethod
    def from_json(cls, summaryMessage: str, detailedMessage: str, *args, **kwargs) -> PullRequestMergeVeto:
        return cls(summary_message=summaryMessage, detailed_message=detailedMessage)


@dataclass(frozen=True)
class BitbucketCompositeError(Exception):
    errors: List[BitbucketError]

    def __str__(self) -> str:
        return str([str(error) for error in self.errors])

    @classmethod
    def check(cls, j):
        if isinstance(j, dict) and "errors" in j:
            raise BitbucketCompositeError.from_json(**j)

    # noinspection PyPep8Naming
    @classmethod
    def from_json(cls, errors: List, *args, **kwargs) -> BitbucketCompositeError:
        return cls(errors=[BitbucketError.from_json(**error) for error in errors])


@dataclass(frozen=True)
class BitbucketError:
    context: str
    message: str
    exception_name: str

    def __str__(self) -> str:
        return self.message

    # noinspection PyPep8Naming
    @classmethod
    def from_json(cls, context: str, message: str, exceptionName: str, *args, **kwargs) -> BitbucketError:
        return cls(context=context, message=message, exception_name=exceptionName)
