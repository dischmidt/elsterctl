# ERiC Integration Notes (Release 43)

This project integrates ERiC through Python `ctypes`.

The scope of `elsterctl` is limited to workflows with German tax offices
through the German ELSTER tax portal.

## Runtime library path

Set `ELSTER_ERIC_LIB` to the absolute path of the ERiC shared library.

Example (macOS):

```bash
export ELSTER_ERIC_LIB=/path/to/eric/lib/libericapi.dylib
```

## Design goals

- Keep all C-level symbols in `infrastructure/eric/bindings.py`.
- Expose stable Python methods through `EricClient`.
- Keep CLI commands independent from low-level `ctypes` details.

## Baseline symbols (current)

The project resolves these lifecycle symbols with fallback names:

- initialize: `EricInitialisiere` or `ericapi_initialize`
- process: `EricBearbeiteVorgang` or `ericapi_process`
- shutdown: `EricBeende` or `ericapi_cleanup`

For this stage, only `restype` is fixed to `int` (`ctypes.c_int`).
Argument signatures are intentionally kept open until the exact
Release 43 header prototypes are added to the repository.

## Next integration step

Add Release 43 headers/constants and lock each function's `argtypes`.
