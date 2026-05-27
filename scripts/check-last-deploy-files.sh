#!/usr/bin/env bash
set -euo pipefail

SITE_ID="${1:-${NETLIFY_SITE_ID:-}}"
if [[ -z "$SITE_ID" ]]; then
  echo "Usage: $0 <site_id>"
  echo "Or set NETLIFY_SITE_ID in the environment."
  exit 1
fi

NETLIFY_BIN="${NETLIFY_BIN:-/opt/buildhome/node-deps/node_modules/.bin/netlify}"
if [[ ! -x "$NETLIFY_BIN" ]]; then
  NETLIFY_BIN="netlify"
fi

latest_deploy_json="$($NETLIFY_BIN api listSiteDeploys --data "{\"site_id\":\"$SITE_ID\",\"per_page\":1}")"

latest_deploy_id="$(printf '%s' "$latest_deploy_json" | node -pe 'const a=JSON.parse(require("fs").readFileSync(0,"utf8")); if(!a.length) process.exit(2); a[0].id')"
deploy_url="$(printf '%s' "$latest_deploy_json" | node -pe 'const a=JSON.parse(require("fs").readFileSync(0,"utf8")); if(!a.length) process.exit(2); a[0].deploy_ssl_url || a[0].deploy_url')"
state="$(printf '%s' "$latest_deploy_json" | node -pe 'const a=JSON.parse(require("fs").readFileSync(0,"utf8")); if(!a.length) process.exit(2); a[0].state')"
branch="$(printf '%s' "$latest_deploy_json" | node -pe 'const a=JSON.parse(require("fs").readFileSync(0,"utf8")); if(!a.length) process.exit(2); a[0].branch || ""')"

if [[ "$state" != "ready" ]]; then
  echo "Latest deploy is not ready (state=$state)."
  exit 2
fi

echo "Checking latest deploy: $latest_deploy_id"
echo "Branch: $branch"
echo "URL: $deploy_url"
echo

mapfile -t files < <(
  find . \
    -path './.git' -prune -o \
    -path './.netlify' -prune -o \
    -path './tmp' -prune -o \
    -type f \
    \( -name '*.html' -o -name '*.css' -o -name '*.js' -o -name '*.svg' -o -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.webp' -o -name '*.gif' -o -name '*.pdf' -o -name '*.woff' -o -name '*.woff2' -o -name '*.ttf' -o -name '*.otf' \) \
    -print | sed 's#^\./##' | sort
)

missing_count=0
root_status="$(curl -s -o /dev/null -w '%{http_code}' "$deploy_url/")"
if [[ "$root_status" == "404" || "$root_status" == "403" || "$root_status" == "000" ]]; then
  echo "MISSING $root_status  / (site root)"
  missing_count=$((missing_count + 1))
fi

for file in "${files[@]}"; do
  encoded_path="${file// /%20}"
  status="$(curl -s -o /dev/null -w '%{http_code}' "$deploy_url/$encoded_path")"
  if [[ "$status" == "404" || "$status" == "403" || "$status" == "000" ]]; then
    echo "MISSING $status  $file"
    missing_count=$((missing_count + 1))
  fi
done

if [[ $missing_count -eq 0 ]]; then
  echo "OK: No missing files detected in latest deploy for scanned asset types."
else
  echo "Found $missing_count missing file(s) in latest deploy."
  exit 3
fi
