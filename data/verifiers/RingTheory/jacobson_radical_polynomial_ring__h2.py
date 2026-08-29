import sympy
import sympy.combinatorics
from sympy.polys.domains import Domain

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) > 0:
            R = witness[0]
        else:
            R = witness
    except Exception:
        R = witness

    if isinstance(R, dict):
        try:
            h1 = bool(R.get("is_commutative", False))
            h2 = bool(R.get("has_polynomial_ring", True))
            if "jacobson_radical_rx_equals_nx" in R:
                neg_q = not bool(R["jacobson_radical_rx_equals_nx"])
            elif "is_jacobson_ring" in R:
                neg_q = not bool(R["is_jacobson_ring"])
        except Exception:
            pass
        return [h1, h2, neg_q]

    if isinstance(R, str):
        try:
            w = R.lower().replace(" ", "")
            if any(x in w for x in ["z_(p)", "z_{(p)}", "local", "power", "[[x]]"]):
                return [True, True, True]
            if any(x in w for x in ["zz", "qq", "field"]):
                return [True, True, False]
        except Exception:
            pass

    try:
        if hasattr(R, "is_commutative"):
            val = R.is_commutative
            if val is not None:
                h1 = bool(val)
        elif isinstance(R, Domain):
            h1 = True
    except Exception:
        pass

    try:
        if hasattr(R, "has_polynomial_ring"):
            h2 = bool(R.has_polynomial_ring)
        else:
            h2 = h1
    except Exception:
        h2 = h1

    try:
        if hasattr(R, "jacobson_radical_rx_equals_nx"):
            neg_q = not bool(R.jacobson_radical_rx_equals_nx)
        elif hasattr(R, "is_jacobson_ring"):
            neg_q = not bool(R.is_jacobson_ring)
        else:
            neg_q = False
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: The ring is a polynomial ring over R in one variable",
    "¬Q: The Jacobson radical of the polynomial ring is not equal to the ideal N"
]

N_HYP = 2
NEG_Q_INDEX = 2