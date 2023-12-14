import os
import json
import random

import typer
from termgraph.module import Data, BarChart, Args, Colors

from github_api_controller import GitHubApiController

base_path = os.path.dirname(os.path.abspath(__file__))


# 1. user의 repository들의 언어 통계
# 2. user의 최근 commit들의 언어 통계
#   2.1 "commit의 언어" 정의
#   2.2 commit의 통계

def main(username: str, token: str):
    github_client = GitHubApiController(token)

    total_language_stats = github_client.get_user_language_stats_by_owning_repos(username)

    render_bar_chart("Language Bar Chart", BarChartData(total_language_stats))


class BarChartData:
    def __init__(self, data: dict):
        self.data = []

        for language, percentage in data.items():
            self.data.append(BarChartDataItem(language, percentage))

        self.sort_by_value_desc()

    def sort_by_value_desc(self):
        self.data.sort(key=lambda x: x.value, reverse=True)


class BarChartDataItem:
    def __init__(self, language: str, value: float):
        self.language = language
        self.value = value
        self.color = self.generate_random_color()

    @staticmethod
    def generate_random_color():
        return Colors.Green


def render_bar_chart(title: str, chart_data: BarChartData):
    data_list = []
    label_list = []
    color_list = []

    for data in chart_data.data:
        data_list.append(data.value)
        label_list.append(data.language)
        color_list.append(data.color)

    render_data = Data([[data] for data in data_list], label_list)

    chart = BarChart(
        render_data,
        Args(
            title=title,
            colors=color_list,
            space_between=True
        )
    )

    chart.draw()


if __name__ == "__main__":
    typer.run(main)
