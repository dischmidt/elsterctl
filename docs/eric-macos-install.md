# ERiC on macOS: package placement and installation

This project expects a local ERiC installation and uses `ctypes` to load
the native library.

The scope of `elsterctl` is limited to workflows with German tax offices
through the German ELSTER tax portal.

## 1) Place the ERiC package in the repository

Store the downloaded ERiC package archive in:

- `vendor/eric/inbox/`

Example:

```bash
cp ~/Downloads/eric_43_*.zip vendor/eric/inbox/
```

## 2) Extract into local runtime directory

Extract package contents into:

- `vendor/eric/runtime/`

Example:

```bash
unzip vendor/eric/inbox/eric_43_*.zip -d vendor/eric/runtime/
```

## 3) Identify the ERiC shared library file

For macOS, use the ERiC dynamic library file (`*.dylib`) from the
extracted runtime.

Typical candidate names include:

- `libericapi.dylib`
- `libericapi_*.dylib`

Use this command to find candidates:

```bash
find vendor/eric/runtime -type f -name "*.dylib"
```

## 4) Export library path for `elsterctl`

Set `ELSTER_ERIC_LIB` to the absolute path of the selected `.dylib`:

```bash
export ELSTER_ERIC_LIB="$(pwd)/vendor/eric/runtime/path/to/libericapi.dylib"
```

Alternative (auto-detect first matching ERiC dylib):

```bash
source scripts/use-local-eric.sh
```

Optional custom runtime dir:

```bash
source scripts/use-local-eric.sh /custom/path/to/runtime
```

Then run:

```bash
elsterctl --help
```

## Notes

- Keep ERiC binary payload out of version control.
- If macOS blocks unsigned libraries, allow execution in system security
  settings as required by your local policy.
- On macOS, it may be necessary to allow access to extracted `.dylib`
  files explicitly, for example:

```bash
xattr -d com.apple.quarantine vendor/eric/runtime/**/*.dylib
```

- If `ctypes` fails with a "library load disallowed by system policy"
  error, remove quarantine attributes from the extracted runtime:

```bash
xattr -dr com.apple.quarantine vendor/eric/runtime/ERiC-43.3.2.0
```

- If the ERiC package includes additional dependency libraries, keep them
  in the same runtime tree so the dynamic linker can resolve them.
