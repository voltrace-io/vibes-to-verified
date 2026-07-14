# Skill Release and Slash-Command Verification

Use this reference when Vibes to Verified is applied to an Agent Skill package, especially one exposing a branded slash command.

## Command identity is platform-specific

- Hermes derives a direct skill command from `SKILL.md` frontmatter `name`. A skill with `name: v2v` resolves as `/v2v` after skill reload/discovery.
- Telegram command menus may translate hyphens to underscores, but Hermes resolves them back to the canonical hyphenated skill key.
- Claude Code commonly derives the skill command from the directory slug under `.claude/skills/`, not only the frontmatter name.
- For a consistent short command across both systems, align all three:
  - frontmatter: `name: v2v`
  - Hermes install directory: `~/.hermes/skills/v2v`
  - Claude directory: `.claude/skills/v2v`

Do not claim the branded command is portable merely because one platform loaded the skill.

## Natural-path proof

A file scan or `skill_view` proves discoverability, not direct command operation. For scoped operational proof, retain:

1. the literal slash invocation
2. the gateway/session read-back showing the intended skill loaded
3. the preserved user instruction
4. the installed `SKILL.md` hash
5. the exact release commit or artifact identifier
6. the platform and reload/discovery path used

One successful invocation supports only that named platform, gateway, profile, and version. General compatibility remains unclaimed until separately exercised.

## Exact-candidate discipline

Keep these identities separate:

- Git `HEAD` commit and tree
- Git index/staged candidate
- mutable working tree
- installed skill copy
- release manifest
- public media bundle

A manifest built from staged Git blobs can correctly match the index while the working tree and installed copy contain newer bytes. Therefore:

1. decide the intended public boundary
2. move private production sources, QC, and intermediates outside that boundary
3. stage the candidate
4. rebuild the manifest from staged blobs
5. rerun validator, tests, privacy scan, lint, compilation, and whitespace checks
6. commit locally
7. record commit, tree, manifest hash, promoted-media hashes, and installed-skill hash
8. run fresh independent reviews against that exact commit

A clean-copy simulation is useful V2 evidence, but it does not make the canonical workspace immutable.

## Public media promotion

When a private production artifact becomes launch media, promote only the intended final file unless reproducible public source is deliberately part of the package.

Required gates:

- exact filename, size, and SHA-256
- full decode and stream contract
- black/freeze/silence checks where applicable
- metadata privacy scan
- sampled-frame or full-playback disclosure review
- exact-audio transcript/privacy review
- provenance and rights wording calibrated to what is actually known
- public alt text/media map
- validator requirement and regression test
- manifest binding

Keep voice references, generated plates, keyframes, private paths, QC notes, and production workspaces private unless explicitly approved and sanitized.

## Refutation sequence

Use two review moments rather than one stale approval:

1. Independent reviewers attack the mutable candidate.
2. Reproduce and repair concrete findings.
3. Freeze and commit the exact candidate.
4. Fresh reviewers inspect the new commit, not the earlier bytes.

If the first review returns RED, that is a useful verified result. Do not soften it to YELLOW merely because most tests passed when a required freeze or publication criterion concretely failed.
