from __future__ import annotations

import os
import sys
from typing import Annotated


import typer
from gql.transport.exceptions import TransportQueryError, TransportServerError

from calc_score import UserContributionCounts
from gh_service import fetch_contributions
from output_writer import build_output, write_output

DEFAULT_REPOSITORY = "oss2026hnu/reposcore-py"

app = typer.Typer(help="reposcore-py CLI")


def split_repository(repository: str) -> tuple[str, str]:
    parts = repository.split("/", maxsplit=1)

    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError("저장소는 owner/repo 형식이어야 합니다.")

    return parts[0], parts[1]


@app.command()
def main(
    repos: Annotated[
        list[str],
        typer.Argument(help="조회할 GitHub 저장소 경로입니다. 예: owner/repo1 owner/repo2"),
    ],
    format: Annotated[
        str,
        typer.Option("--format", "-f", help="출력 파일 형식을 지정합니다. (csv | txt | html)"),
    ] = "txt",
    
    output: Annotated[
        str | None,
        typer.Option("--output", "-o",
            help=(
                "결과를 저장할 출력 디렉터리 경로입니다. "
                "생략하면 파일로 저장하지 않고 stdout에 출력합니다. 예: ./result"
            ),
        ),
    ] = None,
    token: Annotated[
        str | None,
        typer.Option("--token", "-t", help="GitHub Personal Access Token. 미제공 시 GITHUB_TOKEN 환경 변수를 사용합니다."),
    ] = None,
) -> None:
    """Fetch basic repository counts from GitHub GraphQL API."""

    if len(repos) == 0:
        print("오류: 저장소를 하나 이상 입력해주세요.", file=sys.stderr)
        raise typer.Exit(1)
        
    resolved_token = token or os.environ.get("GITHUB_TOKEN")
    if not resolved_token:
        typer.echo("오류: GITHUB_TOKEN 환경 변수 또는 --token 옵션이 필요합니다.", err=True)
        raise typer.Exit(1)
        
    all_contributions: list[list[UserContributionCounts]] = []
    
    for repo in repos:
        try:
            contributions = fetch_contributions(repo, resolved_token)
            all_contributions.append(contributions)
        
        except ValueError as error:
            print(f"오류 ({repo}): {error}", file=sys.stderr)
            raise typer.Exit(1) from error

        except TransportQueryError as error:
            print(f"오류 ({repo}): 저장소를 찾을 수 없습니다. 존재 여부와 권한을 확인하세요. (Detail: {error})", file=sys.stderr)
            raise typer.Exit(3) from error

        except TransportServerError as error:
            status_code = getattr(error, "code", None)

            if status_code in [403, 429]:
                print(f"오류 ({repo}): GitHub API 호출 한도(Rate Limit)를 초과했습니다. 잠시 후 다시 시도하세요. (Status: {status_code})", file=sys.stderr)
                raise typer.Exit(2) from error
            elif status_code == 401:
                print(f"오류 ({repo}): GitHub API 인증에 실패했습니다. GITHUB_TOKEN을 확인하세요. (Status: {status_code})", file=sys.stderr)
                raise typer.Exit(4) from error
            else:
                print(f"오류 ({repo}): GitHub 서버 통신 중 HTTP 오류가 발생했습니다. (Status: {status_code})", file=sys.stderr)
                raise typer.Exit(1) from error
        
        except Exception as error:
            print(f"오류 ({repo}): {error}", file=sys.stderr)
            raise typer.Exit(1) from error

def cli() -> None:
    app()


if __name__ == "__main__":
    cli()