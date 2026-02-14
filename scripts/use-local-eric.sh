#!/usr/bin/env zsh

set -euo pipefail

runtime_dir="${1:-vendor/eric/runtime}"

if [[ ! -d "$runtime_dir" ]]; then
  echo "Runtime directory not found: $runtime_dir" >&2
  return 1 2>/dev/null || exit 1
fi

eric_lib="$(find "$runtime_dir" -type f \( -name "libericapi.dylib" -o -name "libericapi_*.dylib" -o -name "*eric*.dylib" \) | head -n 1)"

if [[ -z "$eric_lib" ]]; then
  echo "No ERiC .dylib found under: $runtime_dir" >&2
  echo "Hint: extract the ERiC package into vendor/eric/runtime first." >&2
  return 1 2>/dev/null || exit 1
fi

export ELSTER_ERIC_LIB="$(cd "$(dirname "$eric_lib")" && pwd)/$(basename "$eric_lib")"

echo "ELSTER_ERIC_LIB set to: $ELSTER_ERIC_LIB"
echo "You can now run: elsterctl --help"
