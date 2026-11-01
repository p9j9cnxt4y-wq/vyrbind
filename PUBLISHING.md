# Publication procedure and v0.1.0 release scope

Distribution, import and CLI are `vyrbind`. Private VyrBind commit
`9815abaf2bf872c8ea71ad3c7f9db80daeccbc1f` passed all nine jobs in run
`41258404480`; see the fixed record in RELEASE_EVIDENCE.md. Later revisions
require their own external commit/CI/asset binding. The proposed repository
slug `vyrbind` has not been applied; the existing private repository remains
unchanged. This document does not announce a public release.


Project and publisher brand: **vYronFORGE.**

Copyright (c) 2026 vYronFORGE.

The brand does not assert a legal form. MIT terms are in [LICENSE](LICENSE).
The name VyrBind has not received legal or trademark clearance.
This procedure is not an authorization and is not evidence of publication.

## Release description

VyrBind v0.1.0 is a limited Python reference broker for exclusive creation
of a new UTF-8 text file in a host-bound workspace, followed by artifact readback
and a hash-linked SQLite audit trail. Unknown operations are denied. Network,
deployment, credentials and other controlled effects have no executor.
It is not an OpenAI product, OS sandbox, complete AI security solution,
authenticated human-approval service or production-ready agent.

The completed private qualification and historical failures are recorded in
[RELEASE_EVIDENCE.md](RELEASE_EVIDENCE.md). Only a release's exact tag target,
CI record and asset digests identify its approved bytes. Version 0.1.0 alone
does not identify them. No general platform compatibility is promised.

## Gate 1 — final private correction, if needed

1. Review the exact changed paths, full diff, source-map digest, asset digests,
   baseline, public Git identity and privacy findings. Obtain a new explicit
   owner approval for the specific local commit and private fast-forward push.
   Previously consumed gates cannot be reused.
2. Immediately recheck HEAD, clean index, private repository identity and
   remote baseline. Stage only approved paths, make only the approved commit
   and push once without force. If a result is uncertain, read it back before
   considering any further action; do not blindly repeat a write.
3. Independently verify all committed and remote blobs, then all nine configured
   CI jobs for that exact commit, including test counts and skips. Stop on
   failure. No fix commit or CI rerun is implicitly authorized.
4. Bind existing candidate assets to the exact final source bytes. Rebuild and
   recheck changed package inputs; reuse byte-identical test inputs only with
   retained evidence. Keep final commit/run references in the external release
   verification record so source files do not require self-referential updates.

## Gate B — public visibility, reporting, tag and release

Proceed only under a new explicit owner approval that names the exact final
commit, repository, reviewed public history/logs, chosen reporting route,
v0.1.0 tag, release notes, asset filenames/digests and verification actions.

Before that approval:
- Resolve or explicitly assess provenance, applicable third-party terms and
  name risks with the owner. Do not equate a byte hash or brand with ownership.
- Review all history, Actions runs/logs, artifacts and other content that will
  become public; refresh the review if new content appeared.
- Use the owner-confirmed confidential address
  [info@vyronforge.de](mailto:info@vyronforge.de), with monitoring responsibility
  assigned to **Projektinhaber / vYronFORGE.** Follow [SECURITY.md](SECURITY.md).
- Separately verify message delivery and actual receipt by the responsible party.
  Both remain **NOT_RUN** until supported by evidence; address confirmation and
  this documentation change are not delivery or receipt evidence. A test email
  requires explicit authorization. No response deadline or guaranteed handling
  time is promised.
- Treat GitHub Private Vulnerability Reporting (PVR) as optional additional
  functionality. It is not a publication prerequisite and is not claimed active.

Under the separately approved Gate B, the intended order is:

1. Recheck the final bindings and make the approved public visibility change.
2. Only if separately authorized, enable optional GitHub PVR and independently
   verify its setting, reporter-facing private form and notification handling.
   A SECURITY.md file is not activation evidence. An unavailable or unverified
   optional PVR feature does not block release when the chosen email intake is
   verified. Do not send a test report or message without explicit authorization.
3. Retain the delivery and actual receipt evidence for the chosen email intake.
   Stop before tag or release if that verification is missing or invalidated.
   The repository may already be public at this point; the visibility change
   cannot retract copies. No automatic rollback or substitute contact is authorized.
4. Create the new v0.1.0 tag at the exact approved commit only after verifying
   it does not already exist; never move or overwrite an existing tag.
5. Create the approved GitHub release and upload only the approved source ZIP,
   wheel and SHA256SUMS.txt. Include the final commit/CI and validation scope
   in the release record. Download the published assets and compare SHA-256,
   tag target and all public links before declaring completion.

The owner has approved the email address and monitoring responsibility recorded
above for local publication preparation. Delivery and actual receipt are separate
open checks; mailbox operation is not inferred from the brand, address syntax or
documentation. Keep the corresponding evidence in the external release record.
GitHub PVR is optional and any future activation must be verified separately;
there is no requirement to switch visibility merely to establish the chosen
email route. No release occurs until that email intake has been verified and
the distinct publication gate has been explicitly approved.

No deployment, production installation, personal identity disclosure or
unrelated repository changes are part of this procedure.
FORGE_READY != EXECUTION_AUTHORIZED.
