import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness evaluation
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_int(x):
    if isinstance(x, int):
        return True
    if isinstance(x, float):
        return x.is_integer()
    if hasattr(x, 'is_integer'):
        val = x.is_integer
        if callable(val):
            return val()
        return bool(val)
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The true theorem states that for 1/p + 1/q + 1/r < 1 (the hyperbolic case),
    the Fuchsian triangle group Δ(p,q,r) in PSL(2, R) is isomorphic to the given presentation.
    Dropping the hyperbolic hypothesis makes the conjecture false, as the geometric 
    group in PSL(2, R) is either undefined or not isomorphic to the presentation 
    for spherical and Euclidean cases (1/p + 1/q + 1/r >= 1).
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            q = witness.get('q')
            r = witness.get('r')
        else:
            p, q, r = witness
    except Exception:
        return [False, False]
    
    # H_1: p, q, r are integers strictly greater than 1
    try:
        h1 = bool(is_int(p) and is_int(q) and is_int(r) and p > 1 and q > 1 and r > 1)
    except Exception:
        h1 = False
        
    # ¬Q: The conclusion fails (the group is not isomorphic to the presentation).
    # This happens when the triangle group is not hyperbolic, i.e., 1/p + 1/q + 1/r >= 1.
    # We use integer arithmetic to avoid floating point inaccuracies: q*r + p*r + p*q >= p*q*r
    try:
        p_val = int(p)
        q_val = int(q)
        r_val = int(r)
        neg_q = bool(q_val * r_val + p_val * r_val + p_val * q_val >= p_val * q_val * r_val)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p, q, r are integers strictly greater than 1",
    "¬Q: The geometric triangle group is not isomorphic to the presentation (fails for non-hyperbolic cases)"
]

N_HYP = 1
NEG_Q_INDEX = 1