from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import struct
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml
from PIL import Image, PngImagePlugin

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


validate = load_module("v2v_validate", "scripts/validate.py")
privacy = load_module("v2v_privacy", "scripts/privacy_scan.py")


class PackageContractTests(unittest.TestCase):
    def setUp(self):
        self.template = yaml.safe_load(
            (ROOT / "templates" / "evidence-card.yaml").read_text(encoding="utf-8")
        )

    def test_package_validator_passes(self):
        self.assertEqual(validate.validate_package(), [])

    def test_skill_frontmatter(self):
        frontmatter = validate.parse_skill_frontmatter(ROOT / "SKILL.md")
        self.assertEqual(frontmatter["name"], "vibes-to-verified")
        self.assertLessEqual(len(frontmatter["description"]), 1024)

    def test_template_matches_schema(self):
        self.assertEqual(
            validate.validate_card(ROOT / "templates" / "evidence-card.yaml"), []
        )

    def test_template_starts_without_claimed_evidence(self):
        self.assertEqual(self.template["evidence"], [])

    def test_documented_v0_example_matches_schema(self):
        self.assertEqual(
            validate.validate_card(ROOT / "examples" / "evidence-card-v0.yaml"), []
        )

    def test_readme_yaml_example_matches_schema(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        match = re.search(r"## Example Output.*?```yaml\n(.*?)\n```", readme, re.S)
        self.assertIsNotNone(match)
        card = yaml.safe_load(match.group(1))
        validator = validate.Draft202012Validator(
            validate.load_schema(), format_checker=validate.FormatChecker()
        )
        self.assertEqual([error.message for error in validator.iter_errors(card)], [])
        self.assertEqual(validate.validate_semantics(card), [])

    def test_invalid_verdict_fails_schema(self):
        card = copy.deepcopy(self.template)
        card["verdict"] = "MAYBE"
        schema = validate.load_schema()
        validator = validate.Draft202012Validator(schema)
        self.assertTrue(list(validator.iter_errors(card)))

    def test_schema_requires_structured_test_evidence(self):
        card = copy.deepcopy(self.template)
        card["v2v_level"] = "V2"
        card["scope"]["artifact"] = "sha256:final"
        card["evidence"] = [
            {
                "kind": "test",
                "artifact": "tests/test_boundary.py",
                "observed": "One run passed.",
                "supports": ["C-01"],
            }
        ]
        validator = validate.Draft202012Validator(validate.load_schema())
        self.assertTrue(list(validator.iter_errors(card)))

    def test_schema_requires_structured_independent_review(self):
        card = copy.deepcopy(self.template)
        card["v2v_level"] = "V3"
        card["scope"]["artifact"] = "sha256:final"
        card["evidence"] = [
            {
                "kind": "test",
                "artifact": "tests/test_boundary.py",
                "subject_artifact": "sha256:final",
                "procedure": "Run the bounded race fixture.",
                "expected": "Exactly one winner.",
                "observed": "Exactly one winner.",
                "repetitions": 3,
                "supports": ["C-01"],
            },
            {
                "kind": "review",
                "artifact": "reviews/final.json",
                "subject_artifact": "sha256:final",
                "observed": "Looks correct.",
                "supports": ["C-01"],
            },
        ]
        card["claim_dispositions"] = [
            {"claim_id": "C-01", "status": "survived", "evidence": "reviews/final.json"}
        ]
        validator = validate.Draft202012Validator(validate.load_schema())
        messages = [error.message for error in validator.iter_errors(card)]
        self.assertIn("'reviewer' is a required property", messages)
        self.assertIn("'independence' is a required property", messages)
        self.assertIn("'challenge' is a required property", messages)
        self.assertIn("'result' is a required property", messages)

    def test_promotion_evidence_must_support_main_claim(self):
        card = copy.deepcopy(self.template)
        card["v2v_level"] = "V2"
        card["scope"]["artifact"] = "sha256:final"
        card["evidence"] = [
            {
                "kind": "test",
                "artifact": "tests/test_boundary.py",
                "subject_artifact": "sha256:final",
                "procedure": "Run the bounded race fixture.",
                "expected": "Exactly one winner.",
                "observed": "Exactly one winner.",
                "repetitions": 3,
                "supports": ["C-99"],
            }
        ]
        self.assertIn(
            "V2 test evidence must support the card claim_id",
            validate.validate_semantics(card),
        )

    def test_promotion_evidence_must_match_scope_artifact(self):
        card = copy.deepcopy(self.template)
        card["v2v_level"] = "V2"
        card["scope"]["artifact"] = "sha256:final"
        card["evidence"] = [
            {
                "kind": "test",
                "artifact": "tests/test_boundary.py",
                "subject_artifact": "sha256:stale",
                "procedure": "Run the bounded race fixture.",
                "expected": "Exactly one winner.",
                "observed": "Exactly one winner.",
                "repetitions": 3,
                "supports": ["C-01"],
            }
        ]
        self.assertIn(
            "V2 test evidence must match scope.artifact",
            validate.validate_semantics(card),
        )

    def test_green_rejects_open_blockers(self):
        card = copy.deepcopy(self.template)
        card["verdict"] = "GREEN"
        card["open_blockers"] = ["Required external read-back is unavailable."]
        self.assertIn(
            "GREEN requires open_blockers to be empty",
            validate.validate_semantics(card),
        )

    def test_green_rejects_refuted_main_claim(self):
        card = copy.deepcopy(self.template)
        card["verdict"] = "GREEN"
        card["v2v_level"] = "V3"
        card["claim_dispositions"] = [
            {"claim_id": "C-01", "status": "refuted", "evidence": "reviews/final.json"}
        ]
        self.assertIn(
            "GREEN cannot accompany a refuted or blocked main claim",
            validate.validate_semantics(card),
        )

    def test_schema_rejects_v2_without_test_evidence(self):
        card = copy.deepcopy(self.template)
        card["v2v_level"] = "V2"
        card["scope"]["artifact"] = "commit:abc123"
        validator = validate.Draft202012Validator(validate.load_schema())
        self.assertTrue(list(validator.iter_errors(card)))

    def test_schema_rejects_v3_without_review_evidence(self):
        card = copy.deepcopy(self.template)
        card["v2v_level"] = "V3"
        card["scope"]["artifact"] = "commit:abc123"
        card["evidence"] = [
            {
                "kind": "test",
                "artifact": "tests/test_boundary.py",
                "observed": "Controlled test passed.",
                "supports": ["C-01"],
            }
        ]
        validator = validate.Draft202012Validator(validate.load_schema())
        self.assertTrue(list(validator.iter_errors(card)))

    def test_green_v0_is_structurally_valid_but_unverified(self):
        card = copy.deepcopy(self.template)
        card["verdict"] = "GREEN"
        card["open_blockers"] = []
        validator = validate.Draft202012Validator(validate.load_schema())
        self.assertEqual(list(validator.iter_errors(card)), [])
        self.assertEqual(validate.validate_semantics(card), [])

    def test_v2_requires_test_evidence(self):
        card = copy.deepcopy(self.template)
        card["v2v_level"] = "V2"
        card["scope"]["artifact"] = "commit:abc123"
        errors = validate.validate_semantics(card)
        self.assertIn("V2 requires at least one test evidence item", errors)

    def test_v3_requires_review_evidence(self):
        card = copy.deepcopy(self.template)
        card["v2v_level"] = "V3"
        card["scope"]["artifact"] = "commit:abc123"
        card["evidence"] = [
            {
                "kind": "test",
                "artifact": "tests/test_boundary.py",
                "observed": "Controlled test passed.",
                "supports": ["C-01"],
            }
        ]
        errors = validate.validate_semantics(card)
        self.assertIn("V3 requires at least one independent review evidence item", errors)

    def _v4_base_card(self):
        card = copy.deepcopy(self.template)
        card["v2v_level"] = "V4"
        card["verdict"] = "GREEN"
        card["scope"]["artifact"] = "sha256:abc123"
        card["open_blockers"] = []
        card["claim_dispositions"] = [
            {"claim_id": "C-01", "status": "survived", "evidence": "reviews/final.json"}
        ]
        card["evidence"] = [
            {
                "kind": "test",
                "artifact": "tests/test_boundary.py",
                "subject_artifact": "sha256:abc123",
                "procedure": "Run the bounded race fixture.",
                "expected": "Exactly one winner.",
                "observed": "Exactly one winner.",
                "repetitions": 3,
                "supports": ["C-01"],
            },
            {
                "kind": "review",
                "artifact": "reviews/final.json",
                "subject_artifact": "sha256:abc123",
                "reviewer": "independent-reviewer-02",
                "independence": "independent_agent",
                "challenge": "Attempt to falsify authority and stale-artifact boundaries.",
                "result": "survived",
                "observed": "No counterexample survived reproduction.",
                "supports": ["C-01"],
            },
        ]
        return card

    def test_v3_rejects_disclosed_nonindependent_review_for_promotion(self):
        card = self._v4_base_card()
        card["v2v_level"] = "V3"
        card["verdict"] = "BLOCKED"
        card["open_blockers"] = ["Independent review is unavailable."]
        card["evidence"][1]["independence"] = "sequential_blinded_pass"
        errors = validate.validate_semantics(card)
        self.assertIn("V3 requires at least one independent review evidence item", errors)

    def test_v4_requires_operational_proof(self):
        card = self._v4_base_card()
        errors = validate.validate_semantics(card)
        self.assertIn("V4 requires runtime operational proof", errors)
        self.assertIn("V4 requires readback operational proof", errors)

    def test_v4_runtime_without_readback_fails(self):
        card = self._v4_base_card()
        card["operational_proof"] = [
            {
                "kind": "runtime",
                "artifact": "runtime/run-001.log",
                "subject_artifact": "sha256:abc123",
                "natural_path": True,
                "repetition_count": 3,
                "monitoring_observed": True,
                "recovery_visibility": "Recovery state was observable.",
                "observed": "Natural path completed.",
                "supports": ["C-01"],
            }
        ]
        errors = validate.validate_semantics(card)
        self.assertNotIn("V4 requires runtime operational proof", errors)
        self.assertIn("V4 requires readback operational proof", errors)

    def test_schema_rejects_v4_runtime_without_readback(self):
        card = self._v4_base_card()
        card["operational_proof"] = [
            {
                "kind": "runtime",
                "artifact": "runtime/run-001.log",
                "subject_artifact": "sha256:abc123",
                "natural_path": True,
                "repetition_count": 3,
                "monitoring_observed": True,
                "recovery_visibility": "Recovery state was observable.",
                "observed": "Natural path completed.",
                "supports": ["C-01"],
            }
        ]
        validator = validate.Draft202012Validator(validate.load_schema())
        self.assertTrue(list(validator.iter_errors(card)))

    def test_v4_readback_without_runtime_fails(self):
        card = self._v4_base_card()
        card["operational_proof"] = [
            {
                "kind": "readback",
                "artifact": "runtime/readback-001.json",
                "subject_artifact": "sha256:abc123",
                "readback_source": "External state read-back.",
                "observed": "Expected external state was observed.",
                "supports": ["C-01"],
            }
        ]
        errors = validate.validate_semantics(card)
        self.assertIn("V4 requires runtime operational proof", errors)
        self.assertNotIn("V4 requires readback operational proof", errors)

    def test_valid_v4_semantics_pass(self):
        card = self._v4_base_card()
        card["operational_proof"] = [
            {
                "kind": "runtime",
                "artifact": "runtime/run-001.log",
                "subject_artifact": "sha256:abc123",
                "natural_path": True,
                "repetition_count": 3,
                "monitoring_observed": True,
                "recovery_visibility": "Recovery state was observable.",
                "observed": "Natural path completed.",
                "supports": ["C-01"],
            },
            {
                "kind": "readback",
                "artifact": "runtime/readback-001.json",
                "subject_artifact": "sha256:abc123",
                "readback_source": "External state read-back.",
                "observed": "Expected external state was observed.",
                "supports": ["C-01"],
            },
        ]
        validator = validate.Draft202012Validator(
            validate.load_schema(), format_checker=validate.FormatChecker()
        )
        self.assertEqual([error.message for error in validator.iter_errors(card)], [])
        self.assertEqual(validate.validate_semantics(card), [])

    def test_red_v4_is_structurally_and_semantically_valid(self):
        card = self._v4_base_card()
        card["verdict"] = "RED"
        card["claim_dispositions"][0]["status"] = "refuted"
        card["evidence"][1]["result"] = "refuted"
        card["operational_proof"] = [
            {
                "kind": "runtime",
                "artifact": "runtime/run-001.log",
                "subject_artifact": "sha256:abc123",
                "natural_path": True,
                "repetition_count": 3,
                "monitoring_observed": True,
                "recovery_visibility": "Recovery state was observable.",
                "observed": "Natural path reproduced the rejected behavior.",
                "supports": ["C-01"],
            },
            {
                "kind": "readback",
                "artifact": "runtime/readback-001.json",
                "subject_artifact": "sha256:abc123",
                "readback_source": "External state read-back.",
                "observed": "The counterexample was read back.",
                "supports": ["C-01"],
            },
        ]
        validator = validate.Draft202012Validator(
            validate.load_schema(), format_checker=validate.FormatChecker()
        )
        self.assertEqual([error.message for error in validator.iter_errors(card)], [])
        self.assertEqual(validate.validate_semantics(card), [])

    def test_schema_rejects_v4_without_natural_path_fields(self):
        card = self._v4_base_card()
        card["claim_dispositions"] = [
            {"claim_id": "C-01", "status": "survived", "evidence": "reviews/final.json"}
        ]
        card["open_blockers"] = []
        card["operational_proof"] = [
            {
                "kind": "runtime",
                "artifact": "runtime/run-001.log",
                "subject_artifact": "sha256:abc123",
                "observed": "Natural path completed.",
                "supports": ["C-01"],
            },
            {
                "kind": "readback",
                "artifact": "runtime/readback-001.json",
                "subject_artifact": "sha256:abc123",
                "observed": "Expected external state was observed.",
                "supports": ["C-01"],
            },
        ]
        validator = validate.Draft202012Validator(validate.load_schema())
        messages = [error.message for error in validator.iter_errors(card)]
        self.assertIn("'natural_path' is a required property", messages)
        self.assertIn("'repetition_count' is a required property", messages)
        self.assertIn("'monitoring_observed' is a required property", messages)
        self.assertIn("'recovery_visibility' is a required property", messages)
        self.assertIn("'readback_source' is a required property", messages)

    def test_publication_destinations_remain_placeholder_gated(self):
        planned_destination = "github.com/voltrace-io/vibes-to-verified"
        for relative in ["README.md", "article/article.md", "article/launch-copy.md"]:
            text = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                self.assertNotIn(planned_destination, text)
        article = (ROOT / "article" / "article.md").read_text(encoding="utf-8")
        launch = (ROOT / "article" / "launch-copy.md").read_text(encoding="utf-8")
        self.assertIn("{{REPOSITORY_URL}}", article)
        self.assertIn("{{CASE_STUDY_URL}}", article)
        self.assertIn("{{ARTICLE_URL}}", launch)
        self.assertIn("{{REPOSITORY_URL}}", launch)
        social_svg = (ROOT / "media" / "exports" / "github-social-card.svg").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("github.com/", social_svg)

    def test_launch_copy_blocks_fit_x_character_limit(self):
        text = (ROOT / "article" / "launch-copy.md").read_text(encoding="utf-8")
        for section in [
            "Recommended Launch Post",
            "First Reply — Repository",
            "Second Reply — Saveable Scale",
            "Video-Led Alternative",
        ]:
            section_text = text.split(f"## {section}", 1)[1].split("## ", 1)[0]
            block = section_text.split("```text", 1)[1].split("```", 1)[0].strip()
            with self.subTest(section=section):
                self.assertLessEqual(len(block), 280)

    def test_internal_markdown_links_exist(self):
        missing = []
        link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
        for markdown in ROOT.rglob("*.md"):
            for target in link_pattern.findall(markdown.read_text(encoding="utf-8")):
                target = target.split("#", 1)[0].strip()
                if not target or target.startswith(("http://", "https://", "mailto:", "{{")):
                    continue
                resolved = (markdown.parent / target).resolve()
                if not resolved.exists():
                    missing.append(f"{markdown.relative_to(ROOT)} -> {target}")
        self.assertEqual(missing, [])

    def test_svg_exports_are_well_formed(self):
        for path in (ROOT / "media" / "exports").glob("*.svg"):
            with self.subTest(path=path.name):
                ET.parse(path)

    def test_png_exports_have_expected_dimensions(self):
        expected = {
            "article-cover.png": (1600, 900),
            "github-social-card.png": (1280, 640),
            "paper-trading-receipt.png": (1600, 900),
            "v2v-scale.png": (1600, 900),
            "v2v-workflow.png": (1600, 900),
        }
        for name, dimensions in expected.items():
            path = ROOT / "media" / "exports" / name
            with self.subTest(path=name), Image.open(path) as image:
                self.assertEqual(image.size, dimensions)
                self.assertEqual(len(image.getexif()), 0)

    def test_release_manifest_matches_artifacts(self):
        manifest = json.loads((ROOT / "release" / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "local_candidate_not_published")
        self.assertTrue(all(value == "not_approved" for value in manifest["publication_gates"].values()))
        for artifact in manifest["artifacts"]:
            path = ROOT / artifact["path"]
            with self.subTest(path=artifact["path"]):
                self.assertEqual(path.stat().st_size, artifact["size_bytes"])
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), artifact["sha256"])

    def test_release_manifest_covers_every_tracked_file_except_itself(self):
        manifest = json.loads((ROOT / "release" / "manifest.json").read_text(encoding="utf-8"))
        manifested = {item["path"] for item in manifest["artifacts"]}
        tracked = set(
            subprocess.check_output(
                ["git", "ls-files"], cwd=ROOT, text=True
            ).splitlines()
        )
        self.assertEqual(manifested, tracked - {"release/manifest.json"})

    def test_video_export_contract(self):
        path = ROOT / "media" / "exports" / "vibes-to-verified-vertical.mp4"
        output = subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration,size:stream=codec_name,width,height,r_frame_rate",
                "-of",
                "json",
                str(path),
            ],
            text=True,
        )
        payload = json.loads(output)
        stream = payload["streams"][0]
        self.assertEqual(stream["codec_name"], "h264")
        self.assertEqual((stream["width"], stream["height"]), (1080, 1920))
        self.assertEqual(stream["r_frame_rate"], "30/1")
        self.assertGreater(float(payload["format"]["duration"]), 20.0)
        self.assertGreater(int(payload["format"]["size"]), 0)

    def test_privacy_scan_detects_normal_windows_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            separator = "\\"
            leaked_user_path = "C:" + separator + "Users" + separator + "Alice" + separator + "private.txt"
            leaked_work_path = "C:" + separator + "Ai_Work" + separator + "secret" + separator + "config.yaml"
            (root / "leak.md").write_text(
                f"user={leaked_user_path}\nwork={leaked_work_path}\n",
                encoding="utf-8",
            )
            findings = privacy.scan(root)
        self.assertTrue(any("private_windows_user_path" in finding for finding in findings))
        self.assertTrue(any("private_ai_work_path" in finding for finding in findings))

    def test_privacy_scan_reads_plain_text_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            separator = "\\"
            leaked_path = "C:" + separator + "Users" + separator + "Alice" + separator + "notes.txt"
            (root / "requirements-dev.txt").write_text(leaked_path, encoding="utf-8")
            findings = privacy.scan(root)
        self.assertTrue(any("private_windows_user_path" in finding for finding in findings))

    def test_privacy_scan_reads_png_text_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            separator = "\\"
            leaked_path = "C:" + separator + "Users" + separator + "Alice" + separator + "image.png"
            metadata = PngImagePlugin.PngInfo()
            metadata.add_text("Comment", leaked_path)
            Image.new("RGB", (4, 4), "black").save(root / "leak.png", pnginfo=metadata)
            findings = privacy.scan(root)
        self.assertTrue(any("private_windows_user_path" in finding for finding in findings))

    def test_tracked_source_png_has_no_cabx_metadata_chunk(self):
        path = ROOT / "media" / "source" / "hero-base-gpt-image-2.png"
        data = path.read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        chunks = []
        offset = 8
        while offset + 12 <= len(data):
            length = struct.unpack(">I", data[offset : offset + 4])[0]
            chunk_type = data[offset + 4 : offset + 8]
            chunks.append(chunk_type)
            offset += 12 + length
            if chunk_type == b"IEND":
                break
        self.assertNotIn(b"caBX", chunks)

    def test_privacy_scanner_does_not_embed_private_workspace_literal(self):
        source = (ROOT / "scripts" / "privacy_scan.py").read_text(encoding="utf-8")
        encoded_literal = "C:" + "\\\\" + "Ai_Work" + "\\\\"
        self.assertNotIn(encoded_literal, source)

    def test_public_tree_passes_privacy_scan(self):
        self.assertEqual(privacy.scan(ROOT), [])


if __name__ == "__main__":
    unittest.main()
