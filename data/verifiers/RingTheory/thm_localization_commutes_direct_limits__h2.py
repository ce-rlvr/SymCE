import sympy
from sympy import symbols, Rational, Integer

# Top-level setup
x, y, z = symbols('x y z')

def check_attr(witness, attr_name, default=False):
    if isinstance(witness, dict):
        return bool(witness.get(attr_name, default))
    if hasattr(witness, attr_name):
        attr = getattr(witness, attr_name)
        if callable(attr):
            return bool(attr())
        return bool(attr)
    return default

def conditions(witness):
    try:
        h1 = check_attr(witness, "is_directed_system_of_commutative_rings", False)
    except Exception:
        h1 = False

    try:
        h2 = check_attr(witness, "is_R_direct_limit", False)
    except Exception:
        h2 = False

    try:
        h3 = check_attr(witness, "is_S_direct_limit", False)
    except Exception:
        h3 = False

    try:
        neg_q = not check_attr(witness, "is_isomorphic", True)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: (R_i, phi_ij) is a directed system of commutative rings",
    "H_2: R is the direct limit of R_i",
    "H_3: S is the direct limit of S_i",
    "¬Q: The direct limit of the localized rings is not isomorphic to the localized ring S^{-1}R"
]

N_HYP = 3
NEG_Q_INDEX = 3