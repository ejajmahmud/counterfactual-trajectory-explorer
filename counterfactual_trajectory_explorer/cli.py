"""CLI for counterfactual-trajectory-explorer."""
import sys
import argparse
from .explorer import CounterfactualExplorer

def main():
    parser = argparse.ArgumentParser(description="Counterfactual Trajectory Explorer CLI")
    parser.add_argument("--demo", action="store_true", help="Simulate counterfactual tool evaluation")
    args = parser.parse_args()

    if args.demo:
        exp = CounterfactualExplorer()
        base = {"memory": "Target is user #101", "tokens_spent": 100}
        f1 = exp.fork("f_bash", base)
        f2 = exp.fork("f_sql", base)

        r1 = exp.simulate("f_bash", "bash_query", lambda s: ({"memory": s["memory"] + "; queried via bash"}, 0.70, 0.05))
        r2 = exp.simulate("f_sql", "sql_query", lambda s: ({"memory": s["memory"] + "; indexed sql result"}, 0.95, 0.01))

        best = exp.select_best_counterfactual([r1, r2])
        print(f"Optimal counterfactual action: {best.action_name} (Score={best.score}, Cost=${best.cost_estimate})")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
