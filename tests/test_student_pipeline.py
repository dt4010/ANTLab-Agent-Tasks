import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STUDENT_PATH = ROOT / "基础" / "starter" / "student.py"


def load_student():
    spec = importlib.util.spec_from_file_location("student_under_test", STUDENT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StudentPipelineTests(unittest.TestCase):
    def setUp(self):
        self.student = load_student()
        self.question = "哪个版本的阈值被当前记录支持？"
        self.passages = [
            {"id": "P2", "source": "record/page-2", "text": "v2 的阈值为 12 秒。"},
            {"id": "P1", "source": "record/page-1", "text": "v1 的阈值为 30 秒。"},
        ]

    def test_prepare_messages_request_json_and_include_only_supplied_evidence(self):
        messages = self.student.prepare_messages(self.question, self.passages)
        self.assertTrue(messages)
        combined = "\n".join(message["content"] for message in messages)
        self.assertIn(self.question, combined)
        self.assertIn("P1", combined)
        self.assertIn("P2", combined)
        self.assertIn('"answer"', combined)
        self.assertIn('"citations"', combined)
        self.assertNotIn("dev_answers", combined)

    def test_improve_returns_a_deterministic_reordering_of_supplied_passages(self):
        improved = self.student.improve("v1 阈值", self.passages)
        self.assertEqual({item["id"] for item in improved}, {"P1", "P2"})
        self.assertEqual(improved[0]["id"], "P1")
        self.assertEqual(improved[0], self.passages[1])
        self.assertEqual(improved[1], self.passages[0])


if __name__ == "__main__":
    unittest.main()
