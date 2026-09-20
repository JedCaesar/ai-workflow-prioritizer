import unittest

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


if __name__ == "__main__":
    unittest.main()
