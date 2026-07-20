# Exact-candidate verification in non-relocatable repositories

Use this when a V2V review must bind tests to an immutable Git candidate, but the repository contains gitlinks/submodules, unusual tracked path names, or tests that hard-code the live repository root.

## Decision rules

1. **Freeze first.** Record the exact candidate commit and `COMMIT^{tree}` before review. Prior reviews become stale after any byte changes.
2. **Manifest changed blobs.** Record every path in `BASE..COMMIT` with mode, object type, and Git blob SHA. Validate the manifest back against `git ls-tree COMMIT -- <path>`.
3. **Do not overinterpret archive tree mismatch.** A plain `git archive` cannot faithfully reconstruct a commit tree when it contains gitlinks/submodules or path-encoding edge cases. Diagnose missing/extra entries before treating a mismatch as a candidate defect.
4. **Prefer a detached local clone for executable proof.** Clone locally without checkout, detach at the candidate, confirm `HEAD`, tree hash, and clean status, then run tests there.
5. **Neutralize inherited Python contamination.** For the detached test process, clear `PYTHONPATH` and `PYTHONHOME`; set `PYTHONNOUSERSITE=1` and `PYTHONDONTWRITEBYTECODE=1`.
6. **Detect non-relocatable tests.** If discovery reports that a module was imported from the live repository instead of the clone, inspect the test suite for hard-coded absolute roots or runtime imports. Clearing environment variables is not enough when test code itself inserts the live path.
7. **Use a layered proof instead of weakening tests.** When full isolated discovery is blocked by pre-existing non-relocatable tests:
   - run the focused relevant suite in the clean detached clone;
   - prove all tracked source/test bytes exercised by the live full suite match the exact commit;
   - back up mutable ledgers, run the full suite in the live repository, and restore ledgers byte-for-byte;
   - name the isolation limitation and cap the V2V claim if it is load-bearing.
8. **Do not patch product code merely to satisfy the verification harness.** Make the repository relocatable only when that is an accepted product requirement.
9. **Preserve strengthened safety gates.** When a stale test fixture predates a new fail-closed attestation/hash contract, update the fixture with a valid matching contract. Never weaken the production gate to make the old fixture pass.
10. **Timeout is not review evidence.** A background reviewer that times out or returns no durable verdict contributes no V3 promotion. Re-dispatch a bounded exact-commit lane or leave the claim below V3.

## Evidence receipt

Record:

- candidate commit and tree hash;
- changed-blob manifest path and hash;
- detached-clone status and focused test count;
- live full-suite count plus proof that relevant tracked bytes equal the candidate;
- mutable-ledger backup/restore receipt;
- natural runtime invocation and read-back when claiming V4;
- every limitation that prevented stronger isolation.

This is a scoped fallback, not a shortcut. A demonstrated counterexample still blocks GREEN even when every other layer passes.
