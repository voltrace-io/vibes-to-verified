# Editorial and Source Review of an Immutable Release

Use this checklist when independently reviewing a documentation-heavy release candidate, article bundle, launch copy, media package, or approval card.

## Bind the subject first

- Resolve and report the full commit and tree identifiers.
- Read blobs from the named commit, not merely the working tree.
- Confirm whether the manifest covers every tracked artifact except an explicitly self-referential manifest.
- Do not treat a passing test suite as proof that prose claims are current or sourced.

## Refutation passes

### Source accuracy

- Retrieve primary sources independently when possible.
- Verify quoted wording, author/publisher identity, dates, byte size, and hash where recorded.
- Follow redirects and compare claims against the current canonical documentation.
- If a social post is difficult to render, try the platform's public oEmbed endpoint before declaring it unavailable.

### Naming and runtime calibration

- Separate public product title, package/repository slug, skill frontmatter name, installation-directory name, and slash-command identifier.
- Verify which field actually determines command invocation on each platform.
- Runtime claims must name the exercised platform, entry path, repetition count, and untested boundaries. One successful invocation does not establish general compatibility.

### Rights and provenance

- Treat “rights-cleared,” “licensed,” “original,” and similar wording as factual claims requiring a traceable receipt or explicitly reported/private qualification.
- Check whether a blanket repository license could be read as covering embedded third-party media. “Cleared for publication” does not automatically mean redistributable or sublicensable under MIT.
- Require a media-rights note identifying source, applicable terms, redistribution scope, and any license carve-out. If evidence must remain private, say so and soften categorical wording.
- Distinguish reproducible public sources from private production assets and from final rendered outputs.

### Publication gates and placeholders

- Publication placeholders are acceptable only when visibly intentional, regression-protected, and paired with a binding/read-back sequence.
- Verify ordering: publish/read back repository; bind repository and case-study URLs into the article; approve/publish/read back article; then bind the article URL into launch copy.
- Confirm every public action remains closed until its explicit approval gate.

### Editorial consistency

- Cross-check status paragraphs, gate tables, changelog, review dispositions, and approval cards for tense and state contradictions.
- Search for stale words such as “being repaired,” “pending,” “unclaimed,” or old counts after the candidate is described as repaired.
- Re-check prior findings individually; do not infer that a disposition row proves the final bytes contain the repair.

## Verdict discipline

- `RED`: a concrete contradiction, inaccurate statement, unsafe license ambiguity, or failed publication criterion exists.
- `BLOCKED`: required evidence cannot be accessed, so the claim cannot be decided.
- `GREEN`: all required claims survive and publication gates remain correctly represented.

For every surviving issue, return exact `path:line`, the counter-evidence, and the smallest sufficient repair. Report verified repairs separately from blockers so a mostly repaired candidate does not receive an accidental green light.
