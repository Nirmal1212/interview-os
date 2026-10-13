import json
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN_ROOT = os.path.abspath(os.path.join(HERE, ".."))
REPO_ROOT = os.path.abspath(os.path.join(PLUGIN_ROOT, ".."))
MARKETPLACE = os.path.join(REPO_ROOT, ".claude-plugin", "marketplace.json")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class ManifestTests(unittest.TestCase):
    def test_plugin_manifest_parses(self):
        manifest = load(os.path.join(PLUGIN_ROOT, ".claude-plugin", "plugin.json"))
        self.assertEqual(manifest["name"], "mock-code-review")

    def test_marketplace_lists_the_plugin(self):
        marketplace = load(MARKETPLACE)
        entries = {p["name"]: p for p in marketplace["plugins"]}
        self.assertIn("mock-code-review", entries)
        self.assertEqual(entries["mock-code-review"]["source"], "./mock-code-review")

    def test_marketplace_source_resolves_to_plugin_with_skill(self):
        marketplace = load(MARKETPLACE)
        entry = next(p for p in marketplace["plugins"] if p["name"] == "mock-code-review")
        root = os.path.normpath(os.path.join(REPO_ROOT, entry["source"]))
        self.assertTrue(os.path.isfile(os.path.join(root, ".claude-plugin", "plugin.json")))
        self.assertTrue(os.path.isfile(os.path.join(root, "skills", "mock-code-review", "SKILL.md")))

    def test_skill_name_matches_plugin_name(self):
        skill = os.path.join(PLUGIN_ROOT, "skills", "mock-code-review", "SKILL.md")
        with open(skill, encoding="utf-8") as f:
            front = f.read().split("---")[1]
        self.assertIn("name: mock-code-review", front)


if __name__ == "__main__":
    unittest.main()
