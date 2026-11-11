"""Core Counterfactual Trajectory Explorer implementation."""
import copy
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

@dataclass
class SimulationResult:
    fork_id: str
    action_name: str
    final_state: Dict[str, Any]
    score: float
    cost_estimate: float

class TrajectoryFork:
    def __init__(self, fork_id: str, state_snapshot: Dict[str, Any]):
        self.fork_id = fork_id
        self.state = copy.deepcopy(state_snapshot)

class CounterfactualExplorer:
    """Forks agent state to evaluate what-if scenarios without modifying the primary state."""
    
    def __init__(self):
        self.forks: Dict[str, TrajectoryFork] = {}

    def fork(self, fork_id: str, current_state: Dict[str, Any]) -> TrajectoryFork:
        tf = TrajectoryFork(fork_id, current_state)
        self.forks[fork_id] = tf
        return tf

    def simulate(
        self,
        fork_id: str,
        action_name: str,
        action_fn: Callable[[Dict[str, Any]], Tuple[Dict[str, Any], float, float]]
    ) -> SimulationResult:
        """Executes candidate action on forked state. action_fn returns (new_state, score, cost)."""
        tf = self.forks[fork_id]
        new_state, score, cost = action_fn(tf.state)
        tf.state = new_state
        return SimulationResult(
            fork_id=fork_id,
            action_name=action_name,
            final_state=new_state,
            score=score,
            cost_estimate=cost
        )

    def select_best_counterfactual(self, results: List[SimulationResult]) -> SimulationResult:
        # Score-to-cost ratio maximization
        return max(results, key=lambda r: (r.score / max(0.001, r.cost_estimate)))
