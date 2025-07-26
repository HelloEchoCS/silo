import os
import json
from ingestion.types import (
    PullRequest,
    ProcessedPullRequest,
    ProcessedPullRequestWithEmbeddings,
)


def preprocess():
    with open(os.path.join(os.getcwd(), ".data", "raw", "pull_requests.json")) as f:
        data: list[PullRequest] = json.load(f)
        print(len(data))
        valid_prs = [pr for pr in data[:1000] if pr["draft"] is False]
        return [process_gh_pr(pr) for pr in valid_prs]


def process_gh_pr(pr: PullRequest) -> ProcessedPullRequest:
    return {
        "url": pr["url"] or "",
        "number": pr["number"],
        "diff_url": pr["diff_url"] or "",
        "title": pr["title"] or "",
        "state": pr["state"] or "",
        "body": pr["body"] or "",
    }


def get_titles(prs: list[ProcessedPullRequest]):
    return [pr["title"] for pr in prs]


def attach_embeddings(
    prs: list[ProcessedPullRequest], embeddings: list[list[float]]
) -> list[ProcessedPullRequestWithEmbeddings]:
    return [
        ProcessedPullRequestWithEmbeddings(**pr, embedding=embedding)
        for pr, embedding in zip(prs, embeddings)
    ]
