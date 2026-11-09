#!/usr/bin/env bash
# Usage: pr-tested.sh <owner/repo> <sha> [workflow]   (workflow defaults to Test)
# Prints for $GITHUB_OUTPUT: tested=true|false and heads=<merged PR head shas with sha's tree>.
# tested=true only when a merged PR head with sha's tree has its latest pull_request run of
# the workflow concluded success. Fails closed: any gh error logs to stderr, prints
# tested=false, heads= and exits 0.
set -euo pipefail

repo=$1
sha=$2
workflow=${3:-Test}

fail() {
  echo "pr-tested: $1" >&2
  echo tested=false
  echo heads=
  exit 0
}

tree=$(gh api "repos/$repo/git/commits/$sha" --jq .tree.sha) || fail "cannot read commit $sha"
# An unreadable tree must never equal another unreadable tree.
case "$tree" in ''|null) fail "no tree for $sha" ;; esac
prs=$(gh api "repos/$repo/commits/$sha/pulls" \
  --jq '.[] | select(.merged_at != null) | "\(.number) \(.head.sha)"') || fail "cannot list PRs of $sha"

if [ -z "$prs" ]; then
  echo "no merged PR for $sha" >&2
  echo tested=false
  echo heads=
  exit 0
fi

# latest conclusion of workflow $3 for head $2 in repo $1: success|failure|...|pending|absent
latest() {
  gh api "repos/$1/actions/runs?head_sha=$2&event=pull_request&per_page=100" \
    --jq "[.workflow_runs[] | select(.name == $(jq -n --arg w "$3" '$w'))] | sort_by(.run_number) | last
      | if . == null then \"absent\" else (.conclusion // \"pending\") end"
}

tested=false
heads=
while read -r num head; do
  head_tree=$(gh api "repos/$repo/git/commits/$head" --jq .tree.sha) || fail "cannot read PR #$num head $head"
  if [ "$head_tree" != "$tree" ]; then
    echo "PR #$num head ${head:0:7}: tree differs" >&2
    continue
  fi
  c=$(latest "$repo" "$head" "$workflow") || fail "cannot list runs of PR #$num head $head"
  echo "PR #$num head ${head:0:7}: tree matches, $workflow $c" >&2
  heads="${heads:+$heads }$head"
  [ "$c" = success ] && tested=true
done <<<"$prs"

echo "tested=$tested"
echo "heads=$heads"
