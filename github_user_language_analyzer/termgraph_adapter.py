from termgraph.module import Colors, Data, BarChart, Args


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
        self.color = Colors.Green  # 임시로 Green


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
