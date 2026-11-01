# Security Policy

## Scope and supported versions

VyrBind 0.1.0 is an experimental local reference, not a production
security boundary. No maintenance SLA or complete platform acceptance is
asserted. Release availability and exact tested bytes are identified by the
release record; see [RELEASE_EVIDENCE.md](RELEASE_EVIDENCE.md).

## Reporting a vulnerability

The owner-confirmed confidential reporting address is
[info@vyronforge.de](mailto:info@vyronforge.de).
The responsible monitoring party is **Projektinhaber / vYronFORGE.**
(project owner / vYronFORGE.). This names the responsible project role and
publisher brand; it does not disclose a personal identity or assert a legal form.

Send a private email with a subject such as "VyrBind security report". Include
the affected version/commit, impact and a minimal local reproduction using
synthetic data. Do **not** put exploit details, personal data or secrets in
public issues. Do not send credentials or test other people's infrastructure.
Limit the initial message to what is necessary for triage; agree on a suitable
transfer method with the recipient before sending additional sensitive material.

The project owner is responsible for monitoring the mailbox, reviewing incoming
reports and coordinating further information and any disclosure privately with
the reporter. No response deadline, maintenance SLA or guaranteed handling time
is promised.

### Verification status

The address and monitoring responsibility are confirmed by the project owner.
Message delivery and actual receipt by the responsible party remain
**NOT_RUN / separately to be verified**. This policy does not claim that a
message has been delivered, read or acknowledged, or guarantee end-to-end
encryption. No test email may be sent without explicit authorization.
Before publication, record delivery and actual recipient confirmation separately
from this documentation decision.

### Optional additional GitHub reporting

GitHub Private Vulnerability Reporting (PVR) is an optional additional route,
not a prerequisite for the email reporting route or for publication.
This policy does not claim that PVR is enabled. Use "Report a vulnerability"
only if the repository actually presents GitHub's private reporting form.
Any future activation and verification require separate authorization.
If that form is unavailable, use the email address above; do not post sensitive
details publicly.

## Explicit non-guarantees

This package does not harden against an adversary with write access to the host
process, workspace parent, package source or evidence database. It does not
provide OS isolation, authenticated audit signatures, reliable secret screening
or general race freedom. See [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md).
