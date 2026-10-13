import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE_PATH = ROOT / "进阶" / "challenge_b" / "fixed_engine.py"
DATA_PATH = ROOT / "进阶" / "challenge_b" / "data.json"


def load_engine():
    spec = importlib.util.spec_from_file_location("fixed_engine", ENGINE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Engine


class FixedEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Engine = load_engine()
        cls.data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    def test_scope_is_filtered_before_top_k(self):
        engine = self.Engine()
        corpus = [
            {"id": "outside", "doc_id": "beta", "snapshot": "v1", "page": 1,
             "text": "outside", "tags": ["alpha", "beta"]},
            {"id": "inside", "doc_id": "alpha", "snapshot": "v1", "page": 1,
             "text": "inside", "tags": ["alpha"]},
        ]
        result = engine.evaluate(
            {"query": "alpha beta", "doc_ids": ["alpha"], "snapshot": "v1", "k": 1},
            corpus,
            {"answer": "inside", "citations": ["inside"]},
        )
        self.assertEqual([item["id"] for item in result["evidence"]], ["inside"])
        self.assertEqual(result["locator_status"], "valid")

    def test_cache_key_includes_snapshot(self):
        engine = self.Engine()
        first, second = self.data["cases"][:2]
        engine.evaluate(first["request"], self.data["corpus"], first["draft"])
        result = engine.evaluate(second["request"], self.data["corpus"], second["draft"])
        self.assertFalse(result["cache_hit"])
        self.assertEqual([item["id"] for item in result["evidence"]], ["b02"])

    def test_unknown_scope_is_explicit(self):
        engine = self.Engine()
        case = self.data["cases"][6]
        result = engine.evaluate(case["request"], self.data["corpus"], case["draft"])
        self.assertEqual(result["status"], "invalid_scope")
        self.assertEqual(result["evidence"], [])

    def test_citation_locator_does_not_claim_semantic_support(self):
        engine = self.Engine()
        case = self.data["cases"][3]
        result = engine.evaluate(case["request"], self.data["corpus"], case["draft"])
        self.assertEqual(result["locator_status"], "valid")
        self.assertEqual(result["support_status"], "not_checked")


if __name__ == "__main__":
    unittest.main()
