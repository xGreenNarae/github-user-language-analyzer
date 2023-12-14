

GitHub User Language 통계를 분석합니다.

GitHub API 를 사용합니다.(Rate Limit 때문에 토큰이 필요합니다)  
CLI 도구 입니다.  

test 환경: macos, zsh  


## 사용법

...


## 원리

#### 시나리오 1
- 사용자의 공개된 repo를 모두 가져옵니다.  
- 각 repo의 language 통계를 가져옵니다.  
(이 때, programming language 또는 markup language가 하나도 사용되지 않은 repo는 제외합니다.)
- 백분율을 계산하여 합산합니다.  

- TODO: repo의 commit 비중으로 가중치를 줍니다.  

#### 시나리오 2  
- 유저가 owner가 아닌 repo들에 대한 통계를 포함합니다.  


