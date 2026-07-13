# Security and Privacy

Vibes to Verified is a process specification and validation package. It does not require credentials, network access, or privileged execution.

## Reporting a Problem

After the public repository exists, use a private GitHub security advisory for vulnerabilities that could expose secrets, bypass disclosure boundaries, or promote evidence incorrectly. Do not place sensitive reproduction data in a public issue.

For ordinary documentation or validation defects, open a public issue with a sanitized example.

## Public Disclosure Rules

Do not submit:

- credentials, API keys, cookies, or tokens
- account, identity, medical, or financial data
- private repository paths or infrastructure identifiers
- proprietary strategies, thresholds, or operational schedules
- exploit details that create avoidable risk

A useful report includes:

- the atomic claim
- expected and observed behavior
- minimum sanitized reproduction
- affected artifact version or hash
- proposed maximum supported V2V level

## Automated Disclosure Scan

`scripts/privacy_scan.py` requires a Git-tracked release boundary, scans UTF-8 and BOM-marked UTF-16 text for known secret and private-path patterns, inspects PNG text/EXIF/C2PA-related metadata, and inspects video tags through `ffprobe`. It fails closed when tracked-file enumeration or supported media inspection cannot run. Other NUL-containing or undecodable binary formats are not semantically inspected.

This automation is not a semantic disclosure proof. Strategy details, proprietary thresholds, operational schedules, account context, and exploitable procedures still require a human review against the rules above.

## Trust Boundary

Installing this skill changes agent instructions; it does not itself prove that an agent, model, plugin, test suite, or external integration is trustworthy. Review the final artifacts and authority granted in your own environment.
