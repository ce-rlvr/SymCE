import sympy
import math
import itertools
import functools

class MetricSpace:
    def __init__(self, name, is_metric, is_separable):
        self.name = name
        self.is_metric = is_metric
        self.is_separable = is_separable
        
    def __str__(self):
        return self.name

# Top-level setup: named object bindings that the witness expression may reference.
R_discrete = MetricSpace("R_discrete", True, False)
l_infty = MetricSpace("l_infty", True, False)
R_standard = MetricSpace("R_standard", True, True)
l_2 = MetricSpace("l_2", True, True)
l_1 = MetricSpace("l_1", True, True)
c_0 = MetricSpace("c_0", True, True)
discrete_uncountable = MetricSpace("discrete_uncountable", True, False)
discrete_countable = MetricSpace("discrete_countable", True, True)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False

    try:
        if hasattr(witness, 'is_metric') and hasattr(witness, 'is_separable'):
            h1 = bool(witness.is_metric)
            neg_q = not bool(witness.is_separable)
            return [h1, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, str):
            w = witness.lower().replace(" ", "_")
            if w in ["r_discrete", "l_infty", "discrete_uncountable"]:
                return [True, True]
            if w in ["r", "r_standard", "l_2", "l_1", "c_0", "discrete_countable"]:
                return [True, False]
    except Exception:
        pass

    try:
        if isinstance(witness, sympy.Set):
            # Standard subsets of R^n with the Euclidean metric are metric spaces and separable
            h1 = True
            neg_q = False
            return [h1, neg_q]
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "¬Q: X does not contain a countable dense subset"
]

N_HYP = 1
NEG_Q_INDEX = 1