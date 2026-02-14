# elsterctl

Command-line interface for transmitting messages and tax filings to
German tax authorities via ELSTER (ERiC).

`elsterctl` is a Unix-style CLI designed for programmatic communication
with ELSTER, with a focus on automation, integration, and cross-border
e-commerce workflows.

------------------------------------------------------------------------

## Features

-   Send "other messages" (Sonstige Nachrichten) to tax authorities
-   Submit VAT advance returns (Umsatzsteuer-Voranmeldung)
-   Submit VAT annual returns (Umsatzsteuer-Jahreserklärung)
-   Submit address changes
-   Attach documents to submissions
-   Scriptable and automation-friendly
-   Designed for service providers and technical users

------------------------------------------------------------------------

## Installation

*(TBD --- add binaries, package manager, or build instructions)*

------------------------------------------------------------------------

## Command Structure

    elsterctl <resource> <action> [options]

Primary resources:

-   `message` --- communication with tax authorities
-   `address` --- taxpayer address updates
-   `vat` --- VAT filings
-   `transfer` --- submission tracking and receipts
-   `auth` --- authentication and certificates
-   `config` --- local configuration

------------------------------------------------------------------------

## Commands

### Message Transmission

Send general messages (including attachments) to the tax office.

``` bash
elsterctl message send \
  --tax-number <tax-number> \
  --subject "<subject>" \
  --body <file> \
  --attachment <file>
```

Optional:

``` bash
elsterctl message status --id <transfer-ticket>
elsterctl message list
```

------------------------------------------------------------------------

### Address Update

Submit a change of address.

``` bash
elsterctl address update \
  --tax-number <tax-number> \
  --street "<street>" \
  --postal-code <postal-code> \
  --city "<city>" \
  --country <country-code>
```

------------------------------------------------------------------------

### VAT Advance Return (UStVA)

Submit VAT advance filings.

``` bash
elsterctl vat submit-advance \
  --tax-number <tax-number> \
  --period <YYYY-MM> \
  --data <file>
```

Supported input formats may include XML or JSON (implementation
dependent).

------------------------------------------------------------------------

### VAT Annual Return

Submit VAT annual declarations.

``` bash
elsterctl vat submit-annual \
  --tax-number <tax-number> \
  --year <YYYY> \
  --data <file>
```

------------------------------------------------------------------------

### Authentication

Manage ELSTER certificates and authentication.

``` bash
elsterctl auth login
elsterctl auth certificate import <file>
```

------------------------------------------------------------------------

### Transfer Management

Track submissions and retrieve receipts.

``` bash
elsterctl transfer status <ticket>
elsterctl transfer download-receipt <ticket>
```

------------------------------------------------------------------------

### Configuration

Manage local settings.

``` bash
elsterctl config set <key> <value>
elsterctl config show
```

------------------------------------------------------------------------

## Exit Codes

  Code   Meaning
  ------ ----------------------
  0      Success
  1      General error
  2      Validation error
  3      Transmission failed
  4      Authentication error

*(subject to change)*

------------------------------------------------------------------------

## Roadmap

-   **V1** --- Message transmission with attachments\
-   **V1.1** --- Address change submission\
-   **V2** --- VAT advance returns\
-   **V3** --- VAT annual returns\
-   Future --- background processing, retries, batch workflows

------------------------------------------------------------------------

## Target Users

-   Developers automating ELSTER workflows
-   Tax service providers
-   Cross-border e-commerce operators
-   Technical operators managing German tax submissions

------------------------------------------------------------------------

## Disclaimer

This project is not affiliated with or endorsed by German tax
authorities.

------------------------------------------------------------------------

## License

*(Choose a license --- e.g. MIT, Apache-2.0, etc.)*
