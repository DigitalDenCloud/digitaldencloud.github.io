#!/usr/bin/env bash
#
# Build and test the site content

set -eu

SITE_DIR="_site"
_config="_config.yml"
_baseurl=""

read_baseurl() {
  if [[ $_config == *","* ]]; then
    IFS=","
    read -ra config_array <<<"$_config"
    for ((i = ${#config_array[@]} - 1; i >= 0; i--)); do
      _tmp_baseurl="$(grep '^baseurl:' "${config_array[i]}" | sed "s/.*: *//;s/['\"]//g;s/#.*//")"
      if [[ -n $_tmp_baseurl ]]; then
        _baseurl="$_tmp_baseurl"
        break
      fi
    done
  else
    _baseurl="$(grep '^baseurl:' "$_config" | sed "s/.*: *//;s/['\"]//g;s/#.*//")"
  fi
}

main() {
  if [[ -d $SITE_DIR ]]; then
    rm -rf "$SITE_DIR"
  fi

  read_baseurl

  JEKYLL_ENV=production bundle exec jekyll b \
    -d "$SITE_DIR$_baseurl" -c "$_config"

  bundle exec htmlproofer "$SITE_DIR" \
    --disable-external \
    --ignore-urls "/^http:\/\/127.0.0.1/,/^http:\/\/0.0.0.0/,/^http:\/\/localhost/"
}

main "$@"