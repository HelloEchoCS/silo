from typing import TypedDict


class PullRequest(TypedDict):
    url: str
    number: int
    diff_url: str
    title: str
    state: str
    body: str
    draft: bool


class ProcessedPullRequest(TypedDict):
    url: str
    number: int
    diff_url: str
    title: str
    state: str
    body: str


class ProcessedPullRequestWithEmbeddings(ProcessedPullRequest):
    embedding: list[float]


class RetrievedPullRequest(TypedDict):
    number: int
    title: str
    body: str
    similarity: float
