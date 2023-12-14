import time

import requests


class GitHubApiController:
    def __init__(self, token):
        self.token = token

    def gh_get(self, url):
        headers = {'Authorization': f'Bearer {self.token}'}

        # 실행 시간 측정
        start_time = time.time()
        response = requests.get(url, headers=headers)
        end_time = time.time()

        print(f'API 응답 시간: [{url}] {end_time - start_time:.5f}초')

        return response.json()

    #  https://docs.github.com/ko/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-a-user
    def get_user_repos(self, username) -> list:
        result = []
        page = 1
        # 모든 page를 가져옵니다.
        while True:
            response = self.gh_get(f'https://api.github.com/users/{username}/repos?page={page}&per_page=100')
            if not response:  # TODO: 이렇게 구현하면, 레코드가 100개 미만이더라도 불필요한 요청이 추가로 1회씩 들어갑니다.
                break
            result += response
            page += 1
        return result

    def get_repo_language_stats(self, username, repo_name):
        return self.gh_get(f'https://api.github.com/repos/{username}/{repo_name}/languages')

    def get_user_language_stats_by_owning_repos(self, username) -> dict:
        repos = self.get_user_repos(username)
        language_stats_of_repos = {}
        total_language_stats = {}
        meaningful_repo_count = 0

        # 유의미한 총 repo 개수를 계산하고, repo별 language 통계 데이터를 초기화 합니다.
        for repo in repos:
            repo_name = repo['name']
            result = self.get_repo_language_stats(username, repo_name)

            if not result:  # programming language가 하나도 사용되지 않은 repo
                continue

            language_stats_of_repos[repo_name] = result
            meaningful_repo_count += 1

        # repo별 language 통계 데이터를 총 language 통계 데이터로 합산합니다.
        for repo_name, language_stats in language_stats_of_repos.items():
            total_lines_of_repo = sum(language_stats.values())

            if total_lines_of_repo == 0:
                print(f'Warning: {username}/{repo_name} has no lines of code.')
                continue

            for language, lines_of_language in language_stats.items():
                percentage_of_repo = lines_of_language / total_lines_of_repo * 100  # 백분율

                if percentage_of_repo <= 20:  # 단일 repo에서 20% 이하의 비중을 차지하는 언어는 무시합니다.
                    continue
                if language not in total_language_stats:  # 빈 dict key 생성
                    total_language_stats[language] = 0

                total_language_stats[language] += round(percentage_of_repo / meaningful_repo_count, 2)  # 중요한 연산: 단일 레포의 언어비율을 전체 레포의 언어비율로 환산합니다.

        return total_language_stats
