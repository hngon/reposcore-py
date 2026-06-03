# Python 개발 가이드

이 문서는 reposcore-py 프로젝트에서 Python 코드를 작성할 때 참고할 기본 작성 규칙을 정리합니다.

## 타입 힌트 작성 가이드

타입 힌트는 변수, 함수 매개변수, 반환값의 자료형을 명시하여 코드의 의도를 더 쉽게 파악할 수 있도록 도와줍니다.

타입 힌트를 작성하면 다음과 같은 장점이 있습니다.

- 코드의 입력값과 반환값을 명확히 이해할 수 있습니다.
- Pylance 같은 정적 분석 도구가 타입 오류를 더 쉽게 찾아낼 수 있습니다.
- 협업 시 함수 사용 방법을 빠르게 파악할 수 있습니다.
- 리팩터링 과정에서 잘못된 타입 사용을 줄일 수 있습니다.

## 기본 타입

기본 자료형은 `int`, `str`, `bool`, `float` 등을 사용합니다.

```python
user_id: int = 1
user_name: str = "pangsu12"
is_active: bool = True
score: float = 95.5
```

## 컬렉션 타입

Python 3.9 이상에서는 `list`, `dict`, `set` 같은 기본 컬렉션 타입에 대괄호를 사용하여 내부 타입을 표시할 수 있습니다.

```python
scores: list[int] = [10, 20, 30]
labels: set[str] = {"bug", "documentation"}
user_scores: dict[str, int] = {
    "pangsu12": 100,
    "tester": 80,
}
```

값이 없을 수도 있는 경우에는 `| None`을 사용할 수 있습니다.

```python
github_token: str | None = None
```

## 함수 매개변수 타입

함수의 매개변수에는 변수명 뒤에 `: 타입` 형식으로 타입을 작성합니다.

```python
def get_repo_name(repo_path: str) -> str:
    return repo_path.split("/")[-1]
```

여러 매개변수가 있는 경우 각각 타입을 명시합니다.

```python
def calculate_score(issue_count: int, pr_count: int) -> int:
    return issue_count + pr_count
```

## 반환 타입

함수의 반환 타입은 매개변수 괄호 뒤에 `-> 타입` 형식으로 작성합니다.

```python
def is_valid_repo_path(repo_path: str) -> bool:
    return "/" in repo_path
```

반환값이 없는 함수는 `None`을 사용합니다.

```python
def print_message(message: str) -> None:
    print(message)
```

## 타입 힌트 예시

아래 예시는 저장소 경로 목록을 받아 올바른 `owner/repo` 형식만 반환하는 함수입니다.

```python
def filter_valid_repos(repo_paths: list[str]) -> list[str]:
    valid_repos: list[str] = []

    for repo_path in repo_paths:
        parts = repo_path.split("/")
        if len(parts) == 2 and parts[0] and parts[1]:
            valid_repos.append(repo_path)

    return valid_repos
```

## Pylance와 타입 힌트

Pylance는 VS Code에서 Python 코드를 분석해 주는 도구입니다.

타입 힌트가 작성되어 있으면 Pylance가 다음과 같은 도움을 줄 수 있습니다.

- 잘못된 타입 사용 경고
- 함수 매개변수와 반환 타입 확인
- 자동 완성 정확도 향상
- 코드 작성 중 오류 가능성 조기 발견

따라서 새로 작성하는 함수에는 가능한 한 매개변수 타입과 반환 타입을 명시하는 것을 권장합니다.
