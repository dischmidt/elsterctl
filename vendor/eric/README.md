# Local ERiC package area

Use this folder for local, non-versioned ERiC artifacts.

`elsterctl` uses these artifacts only for workflows with German tax
offices through the German ELSTER tax portal.

- `inbox/`: place downloaded ERiC package archives (`.jar`, `.zip`, `.tar.gz`).
- `runtime/`: unpacked runtime used by local execution.

Typical local flow:

1. Put ERiC package archive in `inbox/`.
2. Extract package into `runtime/`.
3. Set `ELSTER_ERIC_LIB` to the absolute path of the ERiC shared library file.

## Current inbox files and extraction commands

Detected files in `inbox/`:

- `ERiC-43.3.2.0-Darwin-universal.jar`
- `ERiC-43.3.2.0_eSigner-Patch.jar`

Extract them in this order (from repository root):

```bash
rm -rf vendor/eric/runtime/ERiC-43.3.2.0
unzip -o vendor/eric/inbox/ERiC-43.3.2.0-Darwin-universal.jar -d vendor/eric/runtime/
unzip -o vendor/eric/inbox/ERiC-43.3.2.0_eSigner-Patch.jar -d vendor/eric/runtime/
```

Set the library path for `elsterctl`:

```bash
export ELSTER_ERIC_LIB="$(pwd)/vendor/eric/runtime/ERiC-43.3.2.0/Darwin-universal/lib/libericapi.dylib"
```

Or use the helper script:

```bash
source scripts/use-local-eric.sh
```

If loading fails with `library load disallowed by system policy` on
macOS, remove quarantine attributes from the extracted runtime:

```bash
xattr -dr com.apple.quarantine vendor/eric/runtime/ERiC-43.3.2.0
```

The archive and unpacked binaries are intentionally excluded from git.
