import unittest

from fsc_benchmark.metrics import classify, compute_metrics, is_fsc, is_fsc_hard
from fsc_benchmark.models import Classification, GenerationRecord


def rec(**kwargs):
    base = dict(
        sample_id="s",
        model="m",
        task_id="t",
        ecosystem="deployment_context",
        language="python",
        functional_correct=True,
        security_successful=True,
    )
    base.update(kwargs)
    return GenerationRecord.from_dict(base)


class MetricTests(unittest.TestCase):
    def test_is_fsc(self):
        r = rec(functional_correct=True, security_successful=False)
        self.assertTrue(is_fsc(r))
        self.assertEqual(classify(r), Classification.FSC)

    def test_is_fsc_hard(self):
        r = rec(functional_correct=True, security_successful=False, static_flagged=False, dynamic_evidence=True)
        self.assertTrue(is_fsc_hard(r))
        self.assertEqual(classify(r), Classification.FSC_HARD)

    def test_fsc_rate_denominator(self):
        records = [
            rec(sample_id="1", functional_correct=True, security_successful=False),
            rec(sample_id="2", functional_correct=True, security_successful=True),
            rec(sample_id="3", functional_correct=False, security_successful=False),
        ]
        summary = compute_metrics(records)
        self.assertEqual(summary.total, 3)
        self.assertEqual(summary.functional_correct, 2)
        self.assertEqual(summary.fsc_count, 1)
        self.assertAlmostEqual(summary.fsc_rate, 0.5)
        self.assertAlmostEqual(summary.raw_insecure_rate, 2/3)

    def test_no_functionally_correct_outputs(self):
        records = [rec(sample_id="1", functional_correct=False, security_successful=False)]
        summary = compute_metrics(records)
        self.assertIsNone(summary.fsc_rate)


if __name__ == "__main__":
    unittest.main()
