# Publication procedure and v0.1.0 release scope

Local rename candidate: distribution/import/CLI are `vyrbind`; the proposed repository slug `vyrbind` has NOT been applied. The existing private repository is unchanged. Renamed-byte CI is NOT_RUN.


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
- Confirm who receives security reports and monitors notifications.
- Select GitHub Private Vulnerability Reporting as the preferred route, or an
  existing owner-confirmed security address. Do not invent an address.

Under the separately approved Gate B, the intended order is:

1. Recheck the final bindings and make the approved public visibility change.
2. Enable GitHub Private Vulnerability Reporting if selected, then independently
   verify the enabled setting and reporter-facing private form. Confirm the
   responsible recipient and notification handling. A SECURITY.md file alone
   is not evidence of activation. No test report or message is sent unless
   explicitly authorized.
3. Stop before tag or release if reporting verification fails. The repository
   may already be public at this point; the visibility change cannot retract
   copies. No automatic rollback or substitute contact is authorized.
4. Create the new v0.1.0 tag at the exact approved commit only after verifying
   it does not already exist; never move or overwrite an existing tag.
5. Create the approved GitHub release and upload only the approved source ZIP,
   wheel and SHA256SUMS.txt. Include the final commit/CI and validation scope
   in the release record. Download the published assets and compare SHA-256,
   tag target and all public links before declaring completion.

If an existing security address is chosen, verify its responsible recipient and
reachability before publication and obtain approval to put it in SECURITY.md;
that changes source and requires updated bindings. GitHub PVR cannot be
preverified on a private repository. The owner must explicitly accept the
public-switch-to-reporting-verification interval if that route is selected.
No release occurs until the chosen confidential route has been verified.

No deployment, production installation, personal identity disclosure or
unrelated repository changes are part of this procedure.
FORGE_READY != EXECUTION_AUTHORIZED.
