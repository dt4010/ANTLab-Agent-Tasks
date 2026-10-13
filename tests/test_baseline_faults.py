import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHALLENGE_PATH = ROOT / "进阶" / "challenge_b" / "challenge.py"
DATA_PATH = ROOT / "进阶" / "challenge_b" / "data.json"


def load_engine(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Engine


class BaselineFaultTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Engine = load_engine(CHALLENGE_PATH, "baseline_challenge")
        cls.data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    def test_baseline_cache_ignores_snapshot_and_returns_old_evidence(self):
        engine = self.Engine()
        first = self.data["cases"][0]
        second = self.data["cases"][1]
        engine.evaluate(first["request"], self.data["corpus"], first["draft"])
        result = engine.evaluate(second["request"], self.data["corpus"], second["draft"])
        self.assertTrue(result["cache_hit"])
        self.assertEqual([item["id"] for item in result["evidence"]], ["b01"])

    def test_baseline_global_top_k_drops_in_scope_match(self):
        engine = self.Engine()
        corpus = [
            {"id": "outside", "doc_id": "beta", "snapshot": "v1", "page": 1,
             "text": "outside", "tags": ["alpha", "beta"]},
            {"id": "inside", "doc_id": "alpha", "snapshot": "v1", "page": 1,
             "text": "inside", "tags": ["alpha"]},
        ]
        request = {"query": "alpha beta", "doc_ids": ["alpha"], "snapshot": "v1", "k": 1}
        draft = {"answer": "inside", "citations": ["inside"]}
        result = engine.evaluate(request, corpus, draft)
        self.assertEqual(result["evidence"], [])


if __name__ == "__main__":
    unittest.main()
