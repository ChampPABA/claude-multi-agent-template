#!/usr/bin/env bash
# Test suite for pr-tested.sh (fake gh on PATH, real jq applies the --jq filters)
set -euo pipefail

SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/pr-tested.sh"
TMPDIR_TEST=$(mktemp -d)
trap 'rm -rf "$TMPDIR_TEST"' EXIT

mkdir -p "$TMPDIR_TEST/bin"
cat > "$TMPDIR_TEST/bin/gh" << 'GH'
#!/usr/bin/env bash
# fake gh: "gh api <path> --jq <filter>" -> canned JSON in $FAKE_DIR/<path, non-alnum as _>
[ -e "$FAKE_DIR/ERROR" ] && { echo "fake gh: HTTP 500" >&2; exit 1; }
[ "$1" = api ] || exit 2
path=$2; shift 2
filter=.
while [ $# -gt 0 ]; do
  case "$1" in --jq|-q) filter=$2; shift 2 ;; *) shift ;; esac
done
f="$FAKE_DIR/$(printf '%s' "$path" | tr -c 'A-Za-z0-9\n' _)"
[ -f "$f" ] || { echo "fake gh: no canned response for $path" >&2; exit 1; }
jq -r "$filter" "$f"
GH
chmod +x "$TMPDIR_TEST/bin/gh"

PASS=0
FAIL=0
R=o/r
SHA=aaa1111

# new case dir, sets D and FAKE_DIR
newcase() { D="$TMPDIR_TEST/$1"; mkdir -p "$D"; export FAKE_DIR="$D"; }
put() { printf '%s' "$2" > "$D/$(printf '%s' "$1" | tr -c 'A-Za-z0-9\n' _)"; }
tree() { put "repos/$R/git/commits/$1" "{\"tree\":{\"sha\":\"$2\"}}"; }
pulls() { put "repos/$R/commits/$SHA/pulls" "$1"; }
runs() { put "repos/$R/actions/runs?head_sha=$1&event=pull_request&per_page=100" "{\"workflow_runs\":[$2]}"; }
run() { # name number conclusion
  local c=\"$3\"; [ "$3" = null ] && c=null
  printf '{"name":"%s","run_number":%s,"conclusion":%s,"event":"pull_request","head_sha":"x"}' "$1" "$2" "$c"
}
pr() { printf '{"number":%s,"merged_at":"2026-01-01T00:00:00Z","head":{"sha":"%s"}}' "$1" "$2"; }
PR="[$(pr 12 hhh2222)]"

# check <name> <expected stdout> [workflow arg]; the script must always exit 0
check() {
  local name=$1 want=$2 out rc args=("$R" "$SHA")
  [ -n "${3:-}" ] && args+=("$3")
  set +e
  out=$(PATH="$TMPDIR_TEST/bin:$PATH" bash "$SCRIPT" "${args[@]}" 2>"$D/stderr")
  rc=$?
  set -e
  if [ "$rc" -eq 0 ] && [ "$out" = "$want" ]; then
    echo "ok $name"
    PASS=$((PASS + 1))
  else
    echo "FAIL $name: want '$want' rc=0, got '$out' rc=$rc"
    sed 's/^/  stderr: /' "$D/stderr"
    FAIL=$((FAIL + 1))
  fi
}

newcase match
tree $SHA t1; tree hhh2222 t1; pulls "$PR"; runs hhh2222 "$(run Test 1 success)"
check "tree match and success" $'tested=true\nheads=hhh2222'

newcase tree-differs
tree $SHA t1; tree hhh2222 t2; pulls "$PR"; runs hhh2222 "$(run Test 1 success)"
check "tree differs" $'tested=false\nheads='

newcase no-merged-pr
tree $SHA t1; pulls '[{"number":12,"merged_at":null,"head":{"sha":"hhh2222"}}]'
check "no merged PR" $'tested=false\nheads='

newcase latest-failed
tree $SHA t1; tree hhh2222 t1; pulls "$PR"
runs hhh2222 "$(run Test 2 failure),$(run Test 1 success)"
check "latest failure, older success" $'tested=false\nheads=hhh2222'

newcase latest-cancelled
tree $SHA t1; tree hhh2222 t1; pulls "$PR"
runs hhh2222 "$(run Test 1 success),$(run Test 2 cancelled)"
check "latest cancelled" $'tested=false\nheads=hhh2222'

newcase latest-skipped
tree $SHA t1; tree hhh2222 t1; pulls "$PR"
runs hhh2222 "$(run Test 1 success),$(run Test 2 skipped)"
check "latest skipped" $'tested=false\nheads=hhh2222'

newcase latest-running
tree $SHA t1; tree hhh2222 t1; pulls "$PR"
runs hhh2222 "$(run Test 1 success),$(run Test 2 null)"
check "latest still running" $'tested=false\nheads=hhh2222'

newcase no-run
tree $SHA t1; tree hhh2222 t1; pulls "$PR"; runs hhh2222 "$(run Lint 1 success)"
check "no run of that workflow" $'tested=false\nheads=hhh2222'

newcase custom-workflow
tree $SHA t1; tree hhh2222 t1; pulls "$PR"
runs hhh2222 "$(run Test 1 failure),$(run Build 1 success)"
check "custom workflow name" $'tested=true\nheads=hhh2222' Build

newcase second-pr-matches
tree $SHA t1; tree hhh2222 t2; tree ggg3333 t1
pulls "[$(pr 12 hhh2222),$(pr 13 ggg3333)]"
runs ggg3333 "$(run Test 1 success)"
check "first PR mismatches, second matches" $'tested=true\nheads=ggg3333'

newcase heads-only-matching
tree $SHA t1; tree hhh2222 t1; tree ggg3333 t2; tree fff4444 t1
pulls "[$(pr 12 hhh2222),$(pr 13 ggg3333),$(pr 14 fff4444)]"
runs hhh2222 "$(run Test 1 failure)"; runs fff4444 "$(run Test 1 success)"
check "heads lists only tree-matching heads" $'tested=true\nheads=hhh2222 fff4444'

newcase gh-error
tree $SHA t1; tree hhh2222 t1; pulls "$PR"; runs hhh2222 "$(run Test 1 success)"; touch "$D/ERROR"
check "gh error fails closed" $'tested=false\nheads='

newcase gh-error-midway
tree $SHA t1; tree hhh2222 t1; pulls "$PR"
check "runs lookup error fails closed" $'tested=false\nheads='

newcase null-trees
put "repos/$R/git/commits/$SHA" '{"tree":{"sha":null}}'; put "repos/$R/git/commits/hhh2222" '{"tree":{}}'
pulls "$PR"; runs hhh2222 "$(run Test 1 success)"
check "unreadable trees never match" $'tested=false\nheads='

newcase quoted-workflow
tree $SHA t1; tree hhh2222 t1; pulls "$PR"
runs hhh2222 "$(run 'Say \"hi\"' 1 success)"
check "workflow name with a quote" $'tested=true\nheads=hhh2222' 'Say "hi"'

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
