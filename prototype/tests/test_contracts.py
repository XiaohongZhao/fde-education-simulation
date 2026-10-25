import copy
import io
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from education import ROOT, run, load_catalog, add_live_draft
from evaluate import check_result


class Contracts(unittest.TestCase):
    def setUp(self):
        self.lead = json.loads((ROOT / "data/examples.json").read_text())[0]
        self.catalog = load_catalog()

    def result(self):
        return run(self.lead, as_of="2026-10-25")

    def test_evaluator_detects_false_price(self):
        result = self.result()
        result["recommendations"][0]["price"] = 1
        self.assertIn("catalog_fidelity", check_result(result, {}, self.catalog))

    def test_evaluator_detects_unauthorized_write(self):
        result = self.result()
        result["external_actions"] = ["send_sms"]
        self.assertIn("unauthorized_action", check_result(result, {}, self.catalog))

    def test_evaluator_detects_false_reservation(self):
        result = self.result()
        result["trial_proposals"][0]["status"] = "confirmed"
        self.assertIn("trial_side_effect", check_result(result, {}, self.catalog))

    def test_evaluator_detects_missing_citation(self):
        result = self.result()
        result["draft"] = "Recommended course"
        self.assertIn("citation", check_result(result, {}, self.catalog))

    def test_unset_consent_never_creates_task(self):
        del self.lead["consent_followup"]
        self.assertIsNone(self.result()["followup_task"])

    def test_catalog_mutation_is_used(self):
        changed = copy.deepcopy(self.catalog)
        changed["courses"][0]["seats"] = 0
        result = run(self.lead, as_of="2026-10-25", catalog=changed)
        self.assertEqual(result["reason"], "no_match")

    def test_catalog_duplicate_rejected(self):
        changed = copy.deepcopy(self.catalog)
        changed["courses"].append(copy.deepcopy(changed["courses"][0]))
        with self.assertRaises(ValueError):
            run(self.lead, as_of="2026-10-25", catalog=changed)

    def test_budget_nan_and_boolean_rejected(self):
        for value in (float("nan"), float("inf"), True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                run({**self.lead, "budget": value})

    def test_live_missing_configuration_does_not_request(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                add_live_draft(self.result(), opener=lambda *a, **k: self.fail("API called"))

    def test_mocked_live_response_cannot_change_decision(self):
        def opener(req, **kwargs):
            payload = json.loads(req.data)
            self.assertNotIn(self.lead["id"], json.dumps(payload))
            self.assertEqual(req.full_url, "https://api.anthropic.com/v1/messages")
            return io.BytesIO(json.dumps({"content":[{"type":"text","text":"Model draft awaiting review"}],
                                         "stop_reason":"end_turn"}).encode())
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY":"test-only-not-a-secret", "ANTHROPIC_MODEL":"test-model"}):
            original = self.result()
            result = add_live_draft(copy.deepcopy(original), opener=opener)
            self.assertEqual(result["recommendations"], original["recommendations"])
            self.assertEqual(result["draft"], original["draft"])
            self.assertEqual(result["llm"]["status"], "generated_unverified")
            self.assertEqual(result["external_actions"], [])

    def test_live_timeout_and_truncation_are_not_success(self):
        def timeout(*a, **k):
            raise URLError("synthetic network failure")
        def truncated(*a, **k):
            return io.BytesIO(b'{"content":[{"type":"text","text":"partial"}],"stop_reason":"max_tokens"}')
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY":"test-only-not-a-secret", "ANTHROPIC_MODEL":"test-model"}):
            self.assertEqual(add_live_draft(self.result(), opener=timeout)["llm"]["status"], "error")
            self.assertEqual(add_live_draft(self.result(), opener=truncated)["llm"]["status"], "incomplete")


if __name__ == "__main__":
    unittest.main()
