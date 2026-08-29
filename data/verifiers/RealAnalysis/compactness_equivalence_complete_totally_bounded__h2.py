import sympy
from sympy import S, Interval, FiniteSet, Union, Intersection

# Top-level setup: named object bindings that the witness expression may reference.
Reals = S.Reals
Integers = S.Integers
Rationals = S.Rationals

class MetricSpace:
    """A simple class to represent standard metric spaces for the witness."""
    def __init__(self, name, is_metric, is_complete, is_totally_bounded):
        self.name = name
        self.is_metric = is_metric
        self.is_complete = is_complete
        self.is_totally_bounded = is_totally_bounded

R_space = MetricSpace("R", True, True, False)
Q_space = MetricSpace("Q", True, False, False)
Z_space = MetricSpace("Z", True, True, False)
Open01 = MetricSpace("(0, 1)", True, False, True)
Closed01 = MetricSpace("[0, 1]", True, True, True)

def evaluate_witness(witness):
    """Helper to extract properties from the witness."""
    # Handle tuple like (Space, metric)
    if isinstance(witness, tuple) and len(witness) == 2:
        witness = witness[0]
        
    # Handle string names
    if isinstance(witness, str):
        w = witness.lower().replace(" ", "")
        if w in ["r", "reals", "realline"]:
            return True, True, False
        if w in ["q", "rationals"]:
            return True, False, False
        if w in ["z", "integers"]:
            return True, True, False
        if w in ["(0,1)", "openinterval"]:
            return True, False, True
        if w in ["[0,1]", "closedinterval"]:
            return True, True, True

    # Handle custom MetricSpace objects
    if hasattr(witness, "is_metric"):
        return witness.is_metric, witness.is_complete, witness.is_totally_bounded

    # Handle standard SymPy sets
    try:
        if witness == S.Reals:
            return True, True, False
        if witness == S.Integers:
            return True, True, False
        if witness == S.Rationals:
            return True, False, False
    except Exception:
        pass

    # Handle arbitrary SymPy sets (subsets of Reals)
    try:
        is_metric = True
        is_tb = bool(witness.is_bounded)
        is_comp = bool(witness.closure == witness)
        return is_metric, is_comp, is_tb
    except Exception:
        pass

    return False, False, False

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        is_metric, is_comp, is_tb = evaluate_witness(witness)
    except Exception:
        is_metric, is_comp, is_tb = False, False, False
        
    # Hypothesis 1: (X, d) is a metric space
    try:
        h1_ok = bool(is_metric)
    except Exception:
        h1_ok = False
        
    # Negated Conclusion: X is NOT (complete and totally bounded)
    # i.e., X is not complete OR X is not totally bounded.
    try:
        neg_q_ok = not (bool(is_comp) and bool(is_tb))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "¬Q: X is not complete or not totally bounded"
]

N_HYP = 1
NEG_Q_INDEX = 1