"""Fetch daily GitHub contribution stats for the authenticated `gh` user.

Writes data.js (window.STATS = {...}) next to this script, which index.html loads.

Usage:
    python fetch_stats.py                  # last 365 days
    python fetch_stats.py --since 2024-01-01
    python fetch_stats.py --user someone   # another user's public activity
"""
import argparse
import datetime as dt
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      restrictedContributionsCount
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
      commitContributionsByRepository(maxRepositories: 100) {
        repository { nameWithOwner isPrivate primaryLanguage { name color } }
        contributions(first: 100) { nodes { occurredAt commitCount } }
      }
      pullRequestContributions(first: 100) {
        nodes { occurredAt pullRequest { merged } }
      }
      issueContributions(first: 100) { nodes { occurredAt } }
      pullRequestReviewContributions(first: 100) { nodes { occurredAt } }
      repositoryContributions(first: 100) { nodes { occurredAt } }
    }
  }
}
"""

PROFILE_QUERY = """
query($login: String!) {
  user(login: $login) {
    login name avatarUrl url createdAt bio
    followers { totalCount }
    following { totalCount }
    repositories(ownerAffiliations: OWNER, first: 100, orderBy: {field: STARGAZERS, direction: DESC}) {
      totalCount
      nodes { name stargazerCount forkCount isFork isPrivate primaryLanguage { name color } }
    }
  }
}
"""


def gh_graphql(query, **variables):
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        args += ["-F", f"{key}={value}"]
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        sys.exit(f"gh api failed: {result.stderr.strip()}")
    payload = json.loads(result.stdout)
    if payload.get("errors"):
        sys.exit(f"GraphQL errors: {payload['errors']}")
    return payload["data"]


def month_windows(start, end):
    """Yield [from, to) month-sized windows so no nested list exceeds 100 nodes."""
    cur = start
    while cur < end:
        nxt = (cur.replace(day=1) + dt.timedelta(days=32)).replace(day=1)
        yield cur, min(nxt, end)
        cur = nxt


def day_of(timestamp):
    return timestamp[:10]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", help="start date YYYY-MM-DD (default: 365 days ago)")
    parser.add_argument("--user", help="GitHub login (default: the authenticated gh user)")
    parser.add_argument("--out", default=str(Path(__file__).with_name("data.js")))
    parser.add_argument("--hide-private", action="store_true",
                        help="merge private repositories into one anonymous entry (for publishing)")
    opts = parser.parse_args()

    today = dt.date.today()
    start = dt.date.fromisoformat(opts.since) if opts.since else today - dt.timedelta(days=364)
    end = today + dt.timedelta(days=1)
    login = opts.user or gh_graphql("query { viewer { login } }")["viewer"]["login"]

    calendar = {}
    commits = defaultdict(int)
    prs = defaultdict(int)
    prs_merged = defaultdict(int)
    issues = defaultdict(int)
    reviews = defaultdict(int)
    repos_created = defaultdict(int)
    repo_commits = defaultdict(int)
    repo_daily = defaultdict(lambda: defaultdict(int))
    repo_meta = {}
    restricted = 0

    for lo, hi in month_windows(start, end):
        print(f"  {lo:%Y-%m} ...", file=sys.stderr)
        cc = gh_graphql(
            QUERY,
            login=login,
            **{"from": f"{lo}T00:00:00Z", "to": f"{hi - dt.timedelta(days=1)}T23:59:59Z"},
        )["user"]["contributionsCollection"]
        restricted += cc["restrictedContributionsCount"]
        for week in cc["contributionCalendar"]["weeks"]:
            for d in week["contributionDays"]:
                if lo.isoformat() <= d["date"] < hi.isoformat():
                    calendar[d["date"]] = d["contributionCount"]
        for entry in cc["commitContributionsByRepository"]:
            repo = entry["repository"]
            name = repo["nameWithOwner"]
            repo_meta[name] = {
                "private": repo["isPrivate"],
                "language": (repo["primaryLanguage"] or {}).get("name"),
                "color": (repo["primaryLanguage"] or {}).get("color"),
            }
            for node in entry["contributions"]["nodes"]:
                commits[day_of(node["occurredAt"])] += node["commitCount"]
                repo_commits[name] += node["commitCount"]
                repo_daily[name][day_of(node["occurredAt"])] += node["commitCount"]
        for node in cc["pullRequestContributions"]["nodes"]:
            prs[day_of(node["occurredAt"])] += 1
            if node["pullRequest"]["merged"]:
                prs_merged[day_of(node["occurredAt"])] += 1
        for node in cc["issueContributions"]["nodes"]:
            issues[day_of(node["occurredAt"])] += 1
        for node in cc["pullRequestReviewContributions"]["nodes"]:
            reviews[day_of(node["occurredAt"])] += 1
        for node in cc["repositoryContributions"]["nodes"]:
            repos_created[day_of(node["occurredAt"])] += 1

    days = []
    d = start
    while d < end:
        key = d.isoformat()
        known = commits[key] + prs[key] + issues[key] + reviews[key] + repos_created[key]
        total = max(calendar.get(key, 0), known)
        days.append({
            "date": key,
            "commits": commits[key],
            "prs": prs[key],
            "prsMerged": prs_merged[key],
            "issues": issues[key],
            "reviews": reviews[key],
            # Calendar total minus typed contributions: private/restricted work and repo creation.
            "other": total - known + repos_created[key],
            "total": total,
        })
        d += dt.timedelta(days=1)

    repos = [{"name": n, "commits": c, **repo_meta[n], "daily": dict(repo_daily[n])} for n, c in repo_commits.items()]
    if opts.hide_private:
        hidden = {"name": f"{login}/private repos", "commits": 0, "private": True,
                  "language": "Private", "color": None, "daily": defaultdict(int)}
        for r in [r for r in repos if r["private"]]:
            hidden["commits"] += r["commits"]
            for day, count in r["daily"].items():
                hidden["daily"][day] += count
        repos = [r for r in repos if not r["private"]]
        if hidden["commits"]:
            repos.append({**hidden, "daily": dict(hidden["daily"])})

    profile = gh_graphql(PROFILE_QUERY, login=login)["user"]
    own_repos = [r for r in profile["repositories"]["nodes"] if not (opts.hide_private and r["isPrivate"])]
    stats = {
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "profile": {
            "login": profile["login"],
            "name": profile["name"],
            "avatarUrl": profile["avatarUrl"],
            "url": profile["url"],
            "bio": profile["bio"],
            "createdAt": profile["createdAt"],
            "followers": profile["followers"]["totalCount"],
            "following": profile["following"]["totalCount"],
            "repoCount": profile["repositories"]["totalCount"],
            "stars": sum(r["stargazerCount"] for r in own_repos),
            "forks": sum(r["forkCount"] for r in own_repos),
            "topStarred": [
                {"name": r["name"], "stars": r["stargazerCount"]}
                for r in own_repos if not r["isFork"] and r["stargazerCount"] > 0
            ][:5],
        },
        "restrictedContributions": restricted,
        "days": days,
        "repos": sorted(repos, key=lambda r: -r["commits"]),
    }
    Path(opts.out).write_text("window.STATS = " + json.dumps(stats, indent=1) + ";\n", encoding="utf-8")
    print(f"Wrote {opts.out}: {len(days)} days, {sum(x['total'] for x in days)} contributions", file=sys.stderr)


if __name__ == "__main__":
    main()
