# Local Examples

Use this directory for local, non-versioned examples used during
`elsterctl` development (for example ELSTER XML payloads and expected
response notes).

## Recommended local structure

- `messages/` — XML payload examples for message transmission
- `cases/` — short markdown case descriptions (command + expected result)
- `responses/` — captured/sanitized response snippets
- `codes/` — other code or programs using ERiC order interacting with ELSTER
- `docmentations/` — documentations for ELSTER and ERiC

## Important

- Do not commit sensitive tax data, certificates, or credentials.
- Keep real payload files local; only this README is tracked.
