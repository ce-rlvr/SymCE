import sympy
from sympy import CC, QQ, ZZ
from sympy.abc import x, y, z
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: E and F are subfields of L that contain K",
    "H_3: E and F are algebraically disjoint over K",
    "¬Q: E and F are not linearly disjoint over K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample to the conjecture.
    Returns a list of booleans corresponding to the remaining hypotheses and the negated conclusion.
    """
    # 1. Check if witness is a dictionary containing the pre-evaluated properties
    if isinstance(witness, dict):
        try:
            if "K_is_algebraically_closed" in witness:
                return [
                    bool(witness.get("K_is_algebraically_closed", False)),
                    bool(witness.get("E_F_subfields_L_contain_K", False)),
                    bool(witness.get("E_F_algebraically_disjoint_over_K", False)),
                    not bool(witness.get("E_F_linearly_disjoint_over_K", True))
                ]
        except Exception:
            pass

    # 2. Check if witness is an object with attributes for the properties
    try:
        if hasattr(witness, "K_is_algebraically_closed"):
            return [
                bool(getattr(witness, "K_is_algebraically_closed", False)),
                bool(getattr(witness, "E_F_subfields_L_contain_K", False)),
                bool(getattr(witness, "E_F_algebraically_disjoint_over_K", False)),
                not bool(getattr(witness, "E_F_linearly_disjoint_over_K", True))
            ]
    except Exception:
        pass

    # 3. Check if witness is a tuple of mathematical objects (K, E, F, L)
    try:
        K, E, F, L = witness
        
        try:
            h1 = bool(K.is_algebraically_closed())
        except Exception:
            h1 = (K == CC)
            
        try:
            h2 = bool(E.is_subfield(L) and F.is_subfield(L) and K.is_subfield(E) and K.is_subfield(F))
        except Exception:
            h2 = False
            
        try:
            h3 = bool(E.is_algebraically_disjoint(F, K))
        except Exception:
            h3 = False
            
        try:
            neg_q = not bool(E.is_linearly_disjoint(F, K))
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]