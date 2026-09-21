import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "codex_model_router.py"
SPEC = importlib.util.spec_from_file_location("codex_model_router", SCRIPT)
router = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(router)


class CodexModelRouterTests(unittest.TestCase):
    def setUp(self):
        self.policy = router.load_policy(ROOT / "config" / "model-routing.json")

    def test_task_classes_select_expected_current_models(self):
        self.assertEqual(router.candidates_for(self.policy, "simple")[0], {
            "model": "gpt-5.6-luna",
            "effort": "low",
        })
        self.assertEqual(router.candidates_for(self.policy, "standard")[0]["model"], "gpt-5.6-terra")
        self.assertEqual(router.candidates_for(self.policy, "reasoning")[0]["model"], "gpt-5.6-sol")

    def test_fork_command_uses_model_override_without_prompt(self):
        candidate = router.candidates_for(self.policy, "reasoning")[0]
        command = router.build_command(
            "codex", "fork", candidate, Path("/tmp/project"), "session-123"
        )
        self.assertEqual(command[:3], ["codex", "exec", "fork"])
        self.assertIn("gpt-5.6-sol", command)
        self.assertIn('model_reasoning_effort="high"', command)
        self.assertEqual(command[-2:], ["session-123", "-"])

    def test_routed_prompt_prevents_recursive_routing(self):
        prompt = router.routed_prompt("Implement the bounded change", "route-1", "standard")
        self.assertIn(router.CHILD_MARKER, prompt)
        self.assertIn("Do not invoke or delegate to another model-routing adapter", prompt)
        self.assertIn("Implement the bounded change", prompt)

    def test_decision_log_does_not_need_prompt_content(self):
        digest = router.prompt_digest("private bounded task")
        self.assertEqual(len(digest), 64)
        self.assertNotIn("private bounded task", digest)

    def test_unknown_class_is_rejected(self):
        with self.assertRaises(router.RoutingError):
            router.candidates_for(self.policy, "unknown")

    def test_structured_usage_error_is_account_wide(self):
        output = (
            '{"type":"error","message":"You have hit your usage limit."}\n'
            '{"type":"turn.failed","error":{"message":"Purchase more credits."}}\n'
        )
        message = router.structured_error(output)
        self.assertEqual(message, "Purchase more credits.")
        self.assertEqual(router.failure_kind(message), "account-usage-limit")
        self.assertTrue(router.is_global_failure(message))


if __name__ == "__main__":
    unittest.main()
