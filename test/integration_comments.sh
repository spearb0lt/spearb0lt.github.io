#!/usr/bin/env bash
set -euo pipefail

tmp_dir="$(mktemp -d)"
tmp_override="${tmp_dir}/comments-test-override.yml"
tmp_site="${tmp_dir}/site"

cleanup() {
  rm -rf "${tmp_dir}"
}
trap cleanup EXIT

# This site hides the starter's demo collections: `defaults` in _config.yml marks
# posts/books/teachings `published: false`. Jekyll REPLACES (not merges) the
# `defaults` array when configs are layered, so re-declaring it here restores the
# demo posts these assertions run against while keeping the sitemap exclusion.
cat >"${tmp_override}" <<'YAML'
giscus:
  repo: alshedivat/al-folio
  repo_id: R_kgDOExample
  category: Comments
  category_id: DIC_kwDOExample
defaults:
  - scope:
      path: "assets"
    values:
      sitemap: false
YAML

bundle exec jekyll build --config "_config.yml,${tmp_override}" -d "${tmp_site}" >/dev/null

giscus_page="${tmp_site}/blog/2022/giscus-comments/index.html"
disqus_page="${tmp_site}/blog/2015/disqus-comments/index.html"

for page in "${giscus_page}" "${disqus_page}"; do
  if [ ! -f "${page}" ]; then
    echo "comment fixture post was not generated at ${page}" >&2
    echo "  -> is the posts collection still published in this test build?" >&2
    exit 1
  fi
done

grep -q 'https://giscus.app/client.js' "${giscus_page}"
if grep -q 'giscus comments misconfigured' "${giscus_page}"; then
  echo "unexpected giscus misconfiguration warning in ${giscus_page}" >&2
  exit 1
fi

grep -q 'id="disqus_thread"' "${disqus_page}"
grep -q '.disqus.com/embed.js' "${disqus_page}"

echo "comments integration checks passed"
