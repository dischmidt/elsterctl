# elsterctl

Command-line interface for transmitting messages and tax filings to
German tax offices via ELSTER (ERiC).

`elsterctl` is a Unix-style CLI designed for programmatic communication
with ELSTER, with a focus on automation, integration, and cross-border
e-commerce workflows.

The scope of `elsterctl` is limited to German tax offices and the German
ELSTER tax portal.

---

## Terminology

Use the following terms consistently across code, comments, and
documentation:

- Use `German tax office` / `German tax offices`.
- Do not use `tax authority` / `tax authorities`.
- Keep references scoped to German tax offices and the German ELSTER
  tax portal.

For maintainers, see `docs/writing-style.md`.

---

## Features

- Send "other messages" (Sonstige Nachrichten) to German tax offices
- Submit VAT advance returns (Umsatzsteuer-Voranmeldung)
- Submit VAT annual returns (Umsatzsteuer-Jahreserklärung)
- Submit address changes
- Attach documents to submissions
- Scriptable and automation-friendly
- Designed for service providers and technical users

---

## Installation

### Quick Start

Option A (fresh clone):

```bash
git clone <your-repo-url> elsterctl && cd elsterctl
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip && python -m pip install -e .
source scripts/use-local-eric.sh && elsterctl --help
```

If ERiC is not extracted yet, follow the full steps below first.

Option B (already cloned repository):

```bash
cd elsterctl
source .venv/bin/activate || (python3 -m venv .venv && source .venv/bin/activate)
python -m pip install -U pip && python -m pip install -e .
source scripts/use-local-eric.sh && elsterctl --help
```

### Prerequisites

- Python 3.11+
- ERiC Release 43 package (from official ELSTER distribution)
- macOS shell (`zsh`)

### 1) Clone and set up Python environment

```bash
git clone <your-repo-url> elsterctl
cd elsterctl
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

### 2) Place and extract ERiC package locally

This repository uses a local, non-versioned ERiC area:

- `vendor/eric/inbox/` for downloaded archives
- `vendor/eric/runtime/` for extracted runtime files

Copy the package archive and extract it:

```bash
cp ~/Downloads/eric_43_*.zip vendor/eric/inbox/
unzip vendor/eric/inbox/eric_43_*.zip -d vendor/eric/runtime/
```

### 3) Configure ERiC library path

`elsterctl` loads ERiC via `ctypes` and requires the environment variable
`ELSTER_ERIC_LIB` to point to the ERiC dynamic library (`.dylib` on macOS).

Manual example:

```bash
export ELSTER_ERIC_LIB="$(pwd)/vendor/eric/runtime/path/to/libericapi.dylib"
```

Auto-detect helper script:

```bash
source scripts/use-local-eric.sh
```

### 4) Verify setup

```bash
elsterctl --help
python -m pytest -q
```

If no `.dylib` is found, verify that the ERiC archive was extracted under
`vendor/eric/runtime/` and contains the ERiC shared library.

For additional macOS notes, see `docs/eric-macos-install.md`.

### Troubleshooting

- `No ERiC .dylib found under: vendor/eric/runtime`
  - Ensure the archive was extracted into `vendor/eric/runtime/`.
  - Check available libraries: `find vendor/eric/runtime -type f -name "*.dylib"`.

- `Environment variable ELSTER_ERIC_LIB is not set`
  - Run `source scripts/use-local-eric.sh` in the current shell.
  - Or export manually with the absolute `.dylib` path.

- `Failed to load ERiC library`
  - Verify the path points to a real file and not a directory.
  - Ensure dependent ERiC libraries are present in the same runtime tree.

- macOS blocks library loading (Gatekeeper)
  - Open System Settings and allow execution for the blocked binary if prompted.
  - Re-run `source scripts/use-local-eric.sh` and then `elsterctl --help`.

---

## Command Structure

    elsterctl <resource> <action> [options]

Primary resources:

- `message` --- communication with German tax offices
- `address` --- taxpayer address updates
- `vat` --- VAT filings
- `transfer` --- submission tracking and receipts
- `auth` --- authentication and certificates
- `config` --- local configuration

---

## Commands

### Message Transmission

Send general messages (including attachments) to German tax offices.

```bash
elsterctl message send \
  --tax-number <tax-number> \
  --subject "<subject>" \
  --body <file> \
  --attachment <file>
```

Optional:

```bash
elsterctl message status --id <transfer-ticket>
elsterctl message list
```

---

### Address Update

Submit a change of address.

```bash
elsterctl address update \
  --tax-number <tax-number> \
  --street "<street>" \
  --postal-code <postal-code> \
  --city "<city>" \
  --country <country-code>
```

---

### VAT Advance Return (UStVA)

Submit VAT advance filings.

```bash
elsterctl vat submit-advance \
  --tax-number <tax-number> \
  --period <YYYY-MM> \
  --data <file>
```

Supported input formats may include XML or JSON (implementation
dependent).

---

### VAT Annual Return

Submit VAT annual declarations.

```bash
elsterctl vat submit-annual \
  --tax-number <tax-number> \
  --year <YYYY> \
  --data <file>
```

---

### Authentication

Manage ELSTER certificates and authentication.

```bash
elsterctl auth login
elsterctl auth certificate import <file>
```

---

### Transfer Management

Track submissions and retrieve receipts.

```bash
elsterctl transfer status <ticket>
elsterctl transfer download-receipt <ticket>
```

---

### Configuration

Manage local settings.

```bash
elsterctl config set <key> <value>
elsterctl config show
```

---

## Exit Codes

  Code   Meaning
  ------ ----------------------
  0      Success
  1      General error
  2      Validation error
  3      Transmission failed
  4      Authentication error

*(subject to change)*

---

## Roadmap

- **V1** --- Message transmission with attachments
- **V1.1** --- Address change submission
- **V2** --- VAT advance returns
- **V3** --- VAT annual returns
- Future --- background processing, retries, batch workflows

---

## Target Users

- Developers automating ELSTER workflows
- Tax service providers
- Cross-border e-commerce operators
- Technical operators managing German tax submissions

---

## Disclaimer

This project is not affiliated with or endorsed by German tax
authorities.

---

## License

*(Choose a license --- e.g. MIT, Apache-2.0, etc.)*
