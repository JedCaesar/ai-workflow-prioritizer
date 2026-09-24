import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app import assessment_record, load_workflows
from workflow_scorer import Workflow, assess_workflow


class WorkflowScorerTests(unittest.TestCase):
    def test_strong_low_risk_candidate(self):
        workflow = Workflow("Support triage", 5, 20, 5, 5, 1)

        result = assess_workflow(workflow)

        self.assertEqual(result.score, 90)
        self.assertEqual(result.recommendation, "Strong candidate")

    def test_high_risk_workflow_needs_preparation(self):
        workflow = Workflow("Approve medical treatment", 2, 2, 2, 2, 5)

        result = assess_workflow(workflow)

        self.assertLess(result.score, 45)
        self.assertEqual(result.recommendation, "Prepare the foundations")

    def test_rating_outside_range_is_rejected(self):
        workflow = Workflow("Invalid example", 6, 2, 3, 3, 2)

        with self.assertRaises(ValueError):
            assess_workflow(workflow)

    def test_assessment_record_is_ready_for_json(self):
        workflow = Workflow("Support triage", 5, 20, 5, 5, 1)

        record = assessment_record(workflow)

        self.assertEqual(record["workflow"], "Support triage")
        self.assertEqual(record["score"], 90)
        self.assertEqual(record["recommendation"], "Strong candidate")

    def test_load_workflows_reads_csv_rows(self):
        csv_text = (
            "name,frequency,hours_per_week,repetition,data_readiness,risk\n"
            "Support triage,5,20,5,5,1\n"
            "Invoice review,4,10,4,3,2\n"
        )

        with TemporaryDirectory() as directory:
            csv_path = Path(directory) / "workflows.csv"
            csv_path.write_text(csv_text, encoding="utf-8")
            workflows = load_workflows(str(csv_path))

        self.assertEqual(len(workflows), 2)
        self.assertEqual(workflows[0].name, "Support triage")
        self.assertEqual(workflows[1].hours_per_week, 10)


if __name__ == "__main__":
    unittest.main()
