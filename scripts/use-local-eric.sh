#!/usr/bin/env zsh

_use_local_eric() {
  emulate -L zsh
  setopt pipefail
  setopt errexit
  setopt nounset

  runtime_dir="${1:-vendor/eric/runtime}"

  if [[ ! -d "$runtime_dir" ]]; then
    echo "Runtime directory not found: $runtime_dir" >&2
    return 1
  fi

  eric_lib="$(find "$runtime_dir" -type f \( -name "libericapi.dylib" -o -name "libericapi_*.dylib" \) | head -n 1)"

  if [[ -z "$eric_lib" ]]; then
    eric_lib="$(find "$runtime_dir" -type f -name "*eric*.dylib" | head -n 1)"
  fi

  if [[ -z "$eric_lib" ]]; then
    echo "No ERiC .dylib found under: $runtime_dir" >&2
    echo "Hint: extract the ERiC package into vendor/eric/runtime first." >&2
    return 1
  fi

  export ELSTER_ERIC_LIB="$(cd "$(dirname "$eric_lib")" && pwd)/$(basename "$eric_lib")"
  export DYLD_LIBRARY_PATH="$(dirname "$ELSTER_ERIC_LIB")${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"

  echo "ELSTER_ERIC_LIB set to: $ELSTER_ERIC_LIB"
  echo "DYLD_LIBRARY_PATH updated for ERiC dependencies."
  echo "You can now run: elsterctl --help"
}

_use_local_eric "$@"
exit_code=$?
unset -f _use_local_eric 2>/dev/null || true
return "$exit_code" 2>/dev/null || exit "$exit_code"
