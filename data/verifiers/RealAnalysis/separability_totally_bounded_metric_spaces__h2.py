import sympy
import math
import itertools
import functools

class MetricSpace:
    """
    A simple representation of a metric space for formal verification of topological properties.
    """
    def __init__(self, name: str, is_metric_space: bool, is_separable: bool):
        self.name = name
        self.is_metric_space = is_metric_space
        self.is_separable = is_separable

    def __repr__(self):
        return f"MetricSpace({self.name})"

# Top-level setup: Named metric spaces that a witness expression might reference.
DiscreteR = MetricSpace("DiscreteR", is_metric_space=True, is_separable=False)
L_infty = MetricSpace("L_infty", is_metric_space=True, is_separable=False)
R_standard = MetricSpace("R_standard", is_metric_space=True, is_separable=True)
Q_standard = MetricSpace("Q_standard", is_metric_space=True, is_separable=True)
Z_standard = MetricSpace("Z_standard", is_metric_space=True, is_separable=True)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, str):
            w = witness.lower().strip()
            if w in ["discrete_r", "discrete real line", "l_infty", "l^infty", "l_infinity", "discrete metric on r", "discreter"]:
                h1 = True
                neg_q = True
            elif w in ["r", "real line", "r^n", "standard r", "r_standard"]:
                h1 = True
                neg_q = False
        else:
            h1 = bool(witness.is_metric_space)
            neg_q = not bool(witness.is_separable)
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "¬Q: X is not separable"
]

N_HYP = 1
NEG_Q_INDEX = 1