# Contributing

1. Preserve strict source-of-authority boundaries. Never take run/scope/host
   bindings or policy settings from model output.
2. Add a negative test for each new operation and each intended denial path.
3. New effects require an explicit adapter, documented trust boundary, threat
   model update, and independent proof of containment and readback.
4. Do not rename failed/unknown states into `PASS`; do not bypass guards when
   CI reports a failure.
5. Do not add network access, a shell executor, remote service, implicit
   identity, credentials, or a human approval minting path as a convenience.
6. Run `python tools/verify.py` and `python tools/smoke.py` locally before PR.
7. Use synthetic data only. Evidence must not contain personal addresses,
   credentials, private endpoints or real host identifiers.
