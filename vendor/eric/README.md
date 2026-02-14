# Local ERiC package area

Use this folder for local, non-versioned ERiC artifacts.

`elsterctl` uses these artifacts only for workflows with German tax
offices through the German ELSTER tax portal.

- `inbox/`: place downloaded ERiC package archives (zip/tar.gz).
- `runtime/`: unpacked runtime used by local execution.

Typical local flow:

1. Put ERiC package archive in `inbox/`.
2. Extract package into `runtime/`.
3. Set `ELSTER_ERIC_LIB` to the absolute path of the ERiC shared library file.

The archive and unpacked binaries are intentionally excluded from git.
