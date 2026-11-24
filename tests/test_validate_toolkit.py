import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from validate_toolkit import bundled_binaries, main, validate


def load() -> dict:
    return json.loads((ROOT / "toolkit.json").read_text(encoding="utf-8"))


class ValidateToolkitTest(unittest.TestCase):
    def test_repository_manifest_is_valid(self) -> None:
        self.assertEqual(validate(load()), [])

    def test_repository_has_no_bundled_binaries(self) -> None:
        self.assertEqual(bundled_binaries(ROOT), [])

    def test_main_returns_zero_for_repository(self) -> None:
        self.assertEqual(main(["validate", str(ROOT)]), 0)

    def test_rejects_wrong_schema_version(self) -> None:
        self.assertEqual(validate({"schema_version": 2, "tools": []}), ["schema_version must be 1"])

    def test_rejects_non_object_root(self) -> None:
        self.assertEqual(validate([]), ["schema_version must be 1"])

    def test_rejects_empty_tools(self) -> None:
        self.assertEqual(validate({"schema_version": 1, "tools": []}), ["tools must be a non-empty list"])

    def test_rejects_plain_http(self) -> None:
        doc = load()
        doc["tools"][0]["download"] = "http://filezilla-project.org/"
        self.assertIn("tools[0].download: must be an absolute https URL", validate(doc))

    def test_rejects_direct_binary_link(self) -> None:
        doc = load()
        doc["tools"][1]["download"] = "https://example.org/setup.EXE"
        self.assertIn("tools[1].download: must link to the publisher page, not a binary", validate(doc))

    def test_rejects_duplicate_id(self) -> None:
        doc = load()
        doc["tools"].append(copy.deepcopy(doc["tools"][0]))
        self.assertIn(f"tools[{len(doc['tools']) - 1}].id: duplicate 'filezilla'", validate(doc))

    def test_rejects_missing_field(self) -> None:
        doc = load()
        del doc["tools"][2]["safe_use"]
        self.assertIn("tools[2].safe_use: required non-empty string", validate(doc))

    def test_rejects_blank_field(self) -> None:
        doc = load()
        doc["tools"][2]["purpose"] = "   "
        self.assertIn("tools[2].purpose: required non-empty string", validate(doc))

    def test_rejects_unknown_category_and_platform(self) -> None:
        doc = load()
        doc["tools"][2]["category"] = "misc"
        doc["tools"][2]["platforms"] = ["amiga"]
        errors = validate(doc)
        self.assertTrue(any(e.startswith("tools[2].category") for e in errors))
        self.assertTrue(any(e.startswith("tools[2].platforms") for e in errors))

    def test_rejects_non_object_tool(self) -> None:
        doc = load()
        doc["tools"].append("filezilla")
        self.assertIn(f"tools[{len(doc['tools']) - 1}]: must be an object", validate(doc))

    def test_detects_bundled_binary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "toolkit.json").write_text(json.dumps(load()), encoding="utf-8")
            (root / "installer.exe").write_bytes(b"MZ")
            self.assertEqual(bundled_binaries(root), ["installer.exe"])
            self.assertEqual(main(["validate", str(root)]), 1)


if __name__ == "__main__":
    unittest.main()
