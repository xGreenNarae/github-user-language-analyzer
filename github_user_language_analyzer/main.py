import os

import typer

from github_api_controller import GitHubApiController
from github_user_language_analyzer.termgraph_adapter import render_bar_chart, BarChartData

base_path = os.path.dirname(os.path.abspath(__file__))


# 1. user의 repository들의 언어 통계
# 2. user의 최근 commit들의 언어 통계
#   2.1 "commit의 언어" 정의
#   2.2 commit의 통계

def main(username: str, token: str):
    github_client = GitHubApiController(token)

    total_language_stats = github_client.get_user_language_stats_by_owning_repos(username)

    render_bar_chart("Language Bar Chart", BarChartData(total_language_stats))


if __name__ == "__main__":
    typer.run(main)
