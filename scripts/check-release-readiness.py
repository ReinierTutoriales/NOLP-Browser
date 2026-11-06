#!/usr/bin/env python3
"""Fail closed unless mandatory GitHub Actions checks passed on the exact commit."""
import json
import os
import sys
import urllib.error
import urllib.request

REQUIRED = {
    "Security scanning",
    "Security governance",
    "Dependency inventory SBOM",
    "Module boundaries",
    "NOLP governance",
    "Firefox foundation",
}


def main():
    repo = os.environ["GITHUB_REPOSITORY"]
    sha = os.environ["GITHUB_SHA"]
    token = os.environ["GITHUB_TOKEN"]
    api = os.environ.get("GITHUB_API_URL", "https://api.github.com")
    found = {}
    for page in range(1, 6):
        url = f"{api}/repos/{repo}/actions/runs?head_sha={sha}&per_page=100&page={page}"
        request = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
        runs = data.get("workflow_runs", [])
        for run in runs:
            if run.get("head_sha") != sha or run.get("event") not in ("push", "workflow_dispatch"):
                continue
            name = run.get("name")
            if name in REQUIRED:
                found.setdefault(name, []).append(run)
        if len(runs) < 100:
            break

    failures = []
    for name in sorted(REQUIRED):
        runs = found.get(name, [])
        ok = any(run.get("status") == "completed" and run.get("conclusion") == "success" for run in runs)
        print(f"{name}: {'PASS' if ok else 'MISSING/FAILED'}")
        if not ok:
            failures.append(name)
    if failures:
        print("Release blocked: missing or unsuccessful mandatory checks for exact commit.", file=sys.stderr)
        return 1
    print("Release readiness checks passed for", sha)
    return 0


if __name__ == "__main__":
    sys.exit(main())
