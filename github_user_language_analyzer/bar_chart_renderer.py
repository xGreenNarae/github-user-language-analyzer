
# TODO: termgraph에서 지원하지 않는, 레코드 별 색상을 따로 지정하는 기능을 추가하기 위함.
# normalize 등을 직접 구현해야해서 보류.

class BarChartRenderer:
    BLOCK_CHAR = '█'
    DELIMITER = ':'

    def __init__(self, data):
        self.data = data

    def render(self):
        pass
