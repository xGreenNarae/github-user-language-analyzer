import requests


class GitHubApiController:
    def __init__(self, token):
        self.token = token

    def gh_get(self, url):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_user_repos(self, username) -> list:
        return self.gh_get(f'https://api.github.com/users/{username}/repos')

    def get_repo_language_stats(self, username, repo_name):
        return self.gh_get(f'https://api.github.com/repos/{username}/{repo_name}/languages')

    def get_user_language_stats_by_owning_repos(self, username) -> dict:
        repos = self.get_user_repos(username)
        language_stats_of_repos = {}
        total_language_stats = {}
        meaningful_repo_count = 0

        for repo in repos:
            repo_name = repo['name']
            result = self.get_repo_language_stats(username, repo_name)
            if not result:  # programming language가 하나도 사용되지 않은 repo
                continue

            language_stats_of_repos[repo_name] = result
            meaningful_repo_count += 1

        for repo_name, language_stats in language_stats_of_repos.items():
            total_lines_of_repo = sum(language_stats.values())
            for language, lines_of_language in language_stats.items():
                percentage_of_repo = lines_of_language / total_lines_of_repo
                if percentage_of_repo < 0.0001:  # 0.0으로 들어가면 bar chart(termgraph) 에서 오류 발생시킴. --- (참조 1) 반올림 자리수 관리
                    continue
                if language not in total_language_stats:  # 빈 dict key 생성
                    total_language_stats[language] = 0
                total_language_stats[language] += percentage_of_repo / meaningful_repo_count  # 중요한 연산

        # 연산이 끝나면 모든 value를 백분율로 변환한다. xx.yy%
        for language, lines_of_language in total_language_stats.items():
            total_language_stats[language] = round(lines_of_language * 100, 6)  # --- (참조 1) 반올림 자리수 관리

        return total_language_stats
