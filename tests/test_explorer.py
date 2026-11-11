"""Unit tests for counterfactual-trajectory-explorer."""
import unittest
from counterfactual_trajectory_explorer.explorer import CounterfactualExplorer

class TestCounterfactualExplorer(unittest.TestCase):
    def setUp(self):
        self.exp = CounterfactualExplorer()
        self.base_state = {"inventory": 10, "cash": 100}

    def test_fork_isolation(self):
        f = self.exp.fork("fork1", self.base_state)
        f.state["inventory"] = 999
        self.assertEqual(self.base_state["inventory"], 10)  # Primary untouched

    def test_best_selection(self):
        self.exp.fork("f1", self.base_state)
        self.exp.fork("f2", self.base_state)
        r1 = self.exp.simulate("f1", "act1", lambda s: (s, 0.5, 0.10))
        r2 = self.exp.simulate("f2", "act2", lambda s: (s, 0.9, 0.02))
        best = self.exp.select_best_counterfactual([r1, r2])
        self.assertEqual(best.action_name, "act2")
