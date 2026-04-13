#!/usr/bin/env bash
set -euo pipefail

message="${1:-}"
push_flag="${2:-}"

if [[ -z "${message}" ]]; then
  echo "用法: ./git_commit.sh \"提交信息\" [--push]"
  exit 1
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${repo_root}"

if [[ -z "$(git status --porcelain)" ]]; then
  echo "工作区没有变更，无需提交。"
  exit 0
fi

git add -A

if git diff --cached --name-only | grep -E '(^|/)\.env(\.|$)' >/dev/null; then
  echo "检测到 .env 被暂存，已中止提交。"
  echo "请检查 .gitignore 或先执行: git restore --staged .env"
  exit 2
fi

git commit -m "${message}"

git push
