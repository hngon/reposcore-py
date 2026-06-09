from __future__ import annotations

import csv
from html import escape
from io import StringIO
from pathlib import Path
from typing import Any, Literal

from tabulate import tabulate


OutputFormat = Literal["csv", "txt", "html"]


def normalize_output_format(output_format: str) -> OutputFormat:
    normalized = output_format.lower()

    if normalized not in ("csv", "txt", "html"):
        raise ValueError("출력 형식은 csv, txt, html 중 하나여야 합니다.")

    return normalized  # type: ignore[return-value]


def get_repository_name(result: dict[str, Any]) -> str:
    return str(result["nameWithOwner"])


def get_issue_count(result: dict[str, Any]) -> int:
    return int(result["issues"]["totalCount"])


def get_pull_request_count(result: dict[str, Any]) -> int:
    return int(result["pullRequests"]["totalCount"])


def build_txt_output(results: list[dict[str, Any]]) -> str:
    rows = [
        [
            get_repository_name(result),
            get_issue_count(result),
            get_pull_request_count(result),
        ]
        for result in results
    ]

    return tabulate(rows, headers=["repo", "issues", "pull_requests"])


def build_csv_output(results: list[dict[str, Any]]) -> str:
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["repo", "issues", "pull_requests"])

    for result in results:
        writer.writerow(
            [
                get_repository_name(result),
                get_issue_count(result),
                get_pull_request_count(result),
            ]
        )

    return output.getvalue().strip()


def build_html_output(results: list[dict[str, Any]]) -> str:
    rows = "\n".join(
        [
            "      <tr>"
            f"<td>{escape(get_repository_name(result))}</td>"
            f"<td>{get_issue_count(result)}</td>"
            f"<td>{get_pull_request_count(result)}</td>"
            "</tr>"
            for result in results
        ]
    )

    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>reposcore-py result</title>
</head>
<body>
  <table>
    <thead>
      <tr>
        <th>repo</th>
        <th>issues</th>
        <th>pull_requests</th>
      </tr>
    </thead>
    <tbody>
{rows}
    </tbody>
  </table>
</body>
</html>"""


def build_output(results: list[dict[str, Any]], output_format: str) -> str:
    normalized_format = normalize_output_format(output_format)

    if normalized_format == "csv":
        return build_csv_output(results)

    if normalized_format == "html":
        return build_html_output(results)

    return build_txt_output(results)


def write_output(
    content: str,
    output_dir: str | None,
    output_format: str,
) -> Path | None:
    if output_dir is None:
        print(content)
        return None

    normalized_format = normalize_output_format(output_format)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    result_path = output_path / f"results.{normalized_format}"
    result_path.write_text(content, encoding="utf-8")

    return result_path
