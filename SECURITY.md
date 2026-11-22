# Security Policy

## Protection Guidelines
1. Do not commit API credentials, authentication tokens, or client lead data to git.
2. Always execute `python scripts/verify_no_secrets.py` prior to creating commits or PRs.
3. Keep keys isolated in `.env` or `config/credentials.json`, which are excluded by `.gitignore`.

## Reporting Disclosures
To report a potential vulnerability or credential leakage issue, please use GitHub Private Vulnerability Reporting or contact the maintainer directly.
