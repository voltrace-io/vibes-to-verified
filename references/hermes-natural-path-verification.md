# Hermes Natural-Path Skill Verification

Use this when a Vibes to Verified candidate is packaged as a Hermes skill and the claim includes real slash-command execution.

## Command identity

Hermes derives a direct skill command from the SKILL.md frontmatter `name`:

```yaml
name: v2v
```

This produces the native command:

```text
/v2v <instruction>
```

The public product title may remain **Vibes to Verified**. Hermes derives the command from frontmatter and can discover a differently named directory, but Claude Code commonly derives the command from the `.claude/skills/<directory>` slug. For one portable `/v2v` command, align the frontmatter name and both install directories to `v2v`; do not infer cross-platform command identity from a Hermes-only test.

## Verification sequence

1. Install only the intended public/tracked package files into the active profile's skill directory.
2. Run `/reload-skills` rather than restarting the gateway.
3. Require reload read-back to list `v2v` with the expected description.
4. Invoke `/v2v` with a real instruction through the user's natural platform path.
5. Require the gateway to load the full skill, preserve the accompanying instruction, and return an agent result.
6. Independently rescan command resolution when tooling permits and require `v2v` to resolve to `/v2v` and the expected SKILL.md path.
7. Record the platform, profile, installed artifact identity, invocation count, read-back, and limitations.

A successful command lookup alone is V2-style test evidence. The real platform invocation plus observable skill-load/read-back can support V4 within that named Hermes/profile/platform scope.

## Dispatcher and toolset preflight

Before treating a slash-prefixed message as a command test:

1. Confirm the session has the `skills` toolset enabled. A restricted session that reports skills disabled or `0 skills` cannot establish slash-command behavior.
2. Confirm the target skill appears in the active command index or completion surface.
3. Name the interface being tested: gateway, modern TUI, classic REPL, webhook, or noninteractive query. Do not assume those paths share the same dispatcher.
4. Verify that the interface routes the command through Hermes' skill-command builder or dispatcher. A model response to ordinary prompt text beginning with `/v2v` is not dispatch evidence.
5. Preserve the literal command, session ID, skill-load/read-back, installed revision, and final output.

If a constrained test disables the resolver, classify the result as a prompt-following test and rerun through the intended dispatcher. Capture the durable preflight and reroute procedure rather than recording a permanent claim that an interface is broken.

## Output-contract proof is a separate gate

Natural command execution does not establish that the generated artifact satisfies the skill's promised format. When the result is schema-backed:

- capture raw YAML or JSON without Markdown fences when validating the file directly;
- run the package's actual validator and preserve its exit code and output;
- require schema-valid identifiers, evidence records, claim linkage, artifact binding, level-specific fields, limitations, and disclosure boundaries;
- treat visually plausible but schema-invalid output as a reproduced failure;
- repair the skill's output instructions, add regression coverage, install the new exact revision, and rerun the natural path;
- do not build promotional media until the final natural-path output validates.

Discovery, dispatch, execution, schema validity, and operational proof are distinct claims. Report each separately.

## Source tests versus installed-runtime tests

Keep these boundaries separate:

- **Release/package verification:** run validators, Git-manifest checks, privacy scans, and the full contract suite in the source repository or an isolated Git-backed clean candidate.
- **Installed-runtime verification:** test discovery, reload, command resolution, skill loading, instruction preservation, and user-visible response in the active Hermes skill directory.

Do not run Git-bound release tests in a plain installed skill copy and interpret their expected `not a git repository` failures as a runtime defect. Conversely, a successful `/v2v` invocation does not prove that the source manifest, privacy boundary, or immutable release commit is current.

## Candidate-boundary discipline

Before issuing a release-readiness verdict:

- distinguish tracked files, unstaged tracked changes, and untracked production assets;
- decide explicitly whether review videos, QC notes, and production sources are public launch artifacts or private inputs;
- make public package tests enumerate the Git-tracked release boundary, such as through `git ls-files`, instead of recursively ingesting unrelated untracked private archives;
- run directory-wide checks against the intended candidate boundary, not a mixture of tracked release files and unrelated untracked production files;
- after any tracked documentation, test, or skill edit, rebuild and rebind manifests that hash candidate bytes before expecting CI to pass;
- rebuild the manifest only from staged candidate blobs;
- review the exact post-repair bytes.

A functional skill with a stale manifest is not freeze-ready. Keep the runtime verdict and release-readiness verdict separate.
