import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("resolver", ROOT / "skills/model-configuration/scripts/resolve_model.py")
resolver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(resolver)


class ModelResolutionTests(unittest.TestCase):
    def setUp(self):
        self.settings = resolver.read_settings(resolver.DEFAULTS)
        self.runtime = {"can_spawn": True, "can_select_model": True, "can_select_effort": True,
                        "inherits_current_model": True, "current_model": "gpt-6-astra",
                        "models": {"gpt-6-astra": {"efforts": ["high"], "family": "gpt"},
                                   "gpt-6.1-sol": {"efforts": ["high", "xhigh"], "family": "gpt"}}}

    def select(self, role="swarm workers", cross=False):
        return resolver.resolve(self.settings, role, self.runtime, cross)

    def test_default_worker_exact_id_and_inherited_effort(self):
        self.assertEqual(self.select()[0]["parameters"], {"model": "gpt-6.1-sol"})

    def test_unavailable_id_inherits_current_without_guessing(self):
        del self.runtime["models"]["gpt-6.1-sol"]
        seat = self.select()[0]
        self.assertEqual(seat["parameters"], {})
        self.assertEqual(seat["effective_model"], "gpt-6-astra")
        self.assertTrue(any("unavailable" in n for n in seat["notices"]))

    def test_context_restricts_override(self):
        self.runtime["can_select_model"] = False
        self.assertEqual(self.select()[0]["parameters"], {})

    def test_rejected_model_not_retried(self):
        self.runtime["rejected_models"] = ["gpt-6.1-sol"]
        self.assertEqual(self.select()[0]["parameters"], {})

    def test_alias_and_unknown_role(self):
        self.settings["subagents"] = "auto"
        self.assertEqual(self.select("new worker")[0]["parameters"], {})

    def test_effort_separate_and_validated(self):
        self.settings["swarm workers effort"] = "high"
        self.assertEqual(self.select()[0]["parameters"], {"model": "gpt-6.1-sol", "reasoning_effort": "high"})
        self.settings["swarm workers effort"] = "ultra"
        self.assertEqual(self.select()[0]["parameters"], {"model": "gpt-6.1-sol"})

    def test_encoded_effort_not_double_applied(self):
        self.settings["subagent effort"] = "high"
        self.runtime["models"]["gpt-6.1-sol"]["effort_encoded"] = True
        self.assertNotIn("reasoning_effort", self.select()[0]["parameters"])

    def test_panel_preserves_duplicate_seats(self):
        self.assertEqual(len(self.select("arena runners")), 2)
        self.assertEqual(self.select("arena runners")[0]["parameters"], self.select("arena runners")[1]["parameters"])

    def test_same_family_or_unknown_parent_skips_cross_judge(self):
        self.assertEqual(self.select("arena cross-judge pool", True)[0]["action"], "skip-cross-family-judge")
        self.runtime["current_model"] = None
        self.assertEqual(self.select("arena cross-judge pool", True)[0]["action"], "skip-cross-family-judge")

    def test_configured_verified_other_family_can_judge(self):
        self.runtime["models"]["other-provider-id"] = {"family": "other", "efforts": []}
        self.settings["arena cross-judge pool"] = "other-provider-id"
        self.assertEqual(self.select("arena cross-judge pool", True)[0]["parameters"], {"model": "other-provider-id"})

    def test_no_subagent_or_unconfirmed_inheritance_runs_locally(self):
        self.runtime["can_spawn"] = False
        self.assertEqual(self.select()[0]["action"], "run-in-current-session")
        self.assertEqual(self.select()[0]["parameters"], {})
        self.runtime["can_spawn"] = True
        self.runtime["can_select_model"] = False
        self.runtime["inherits_current_model"] = False
        self.assertEqual(self.select()[0]["action"], "run-in-current-session")

    def test_oversight_does_not_switch_main_session(self):
        self.runtime["current_model"] = "gpt-6.1-sol"
        result = self.select("oversight")[0]
        self.assertEqual(result["parameters"], {})
        self.assertEqual(result["effective_model"], "gpt-6.1-sol")
        self.assertEqual(result["action"], "main-session-preference-only")

    def test_custom_oversight_preference_does_not_change_execution(self):
        self.settings["oversight"] = "gpt-6.1-sol"
        self.settings["oversight effort"] = "xhigh"
        result = self.select("oversight")[0]
        self.assertEqual(result["requested_model"], "gpt-6.1-sol")
        self.assertEqual(result["effective_model"], "gpt-6-astra")
        self.assertEqual(result["parameters"], {})

    def test_skipped_judge_has_no_effective_model(self):
        self.assertIsNone(self.select("arena cross-judge pool", True)[0]["effective_model"])

    def test_cli_reads_override_and_runtime_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            settings = directory / "pstack-models.md"
            runtime = directory / "runtime.json"
            settings.write_text("swarm workers: auto\n")
            runtime.write_text(json.dumps(self.runtime))
            command = [sys.executable, str(ROOT / "skills/model-configuration/scripts/resolve_model.py"),
                       "--settings", str(settings), "--runtime", str(runtime), "--role", "swarm workers"]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            parsed = json.loads(result.stdout)
            self.assertEqual(parsed["override"], str(settings))
            self.assertEqual(parsed["selections"][0]["parameters"], {})
            self.assertEqual(parsed["selections"][0]["effective_model"], "gpt-6-astra")

    def test_legacy_frontmatter_and_comma_role_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "rule.mdc"
            p.write_text("---\nalwaysApply: true\n---\n# budget: large (xhigh)\nfeature, refactoring: exact-provider-id\n")
            self.assertEqual(resolver.read_settings(p), {"feature, refactoring": "exact-provider-id"})
            p.write_text("swarm workers: auto\nswarm workers: duplicate\n")
            with self.assertRaises(ValueError):
                resolver.read_settings(p)


if __name__ == "__main__":
    unittest.main()
