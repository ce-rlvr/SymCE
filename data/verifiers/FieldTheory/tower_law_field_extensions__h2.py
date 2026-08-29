import math
import sympy
from sympy import Symbol

class KField:
    """
    A simple class to represent fields and their extensions for the purpose
    of verifying the Tower Law conjecture.
    """
    def __init__(self, name, base=None, deg=1):
        self.name = name
        self.base = base
        self.deg = deg

    def is_subfield(self, other):
        curr = other
        while curr is not None:
            if curr == self:
                return True
            curr = curr.base
        return False

    def degree_over(self, base_field):
        if self == base_field:
            return 1
        curr = self
        deg = 1
        while curr is not None:
            if curr == base_field:
                return deg
            deg *= curr.deg
            curr = curr.base
        return float('inf')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

# Top-level setup: named object bindings that the witness expression may reference.
Q = KField("Q")
Q_x = KField("Q(x)", base=Q, deg=float('inf'))
Q_x_sqrt = KField("Q(x)(sqrt(x))", base=Q_x, deg=2)
Q_sqrt2 = KField("Q(sqrt(2))", base=Q, deg=2)
Q_sqrt2_sqrt3 = KField("Q(sqrt(2), sqrt(3))", base=Q_sqrt2, deg=2)
R = KField("R", base=Q, deg=float('inf'))
C = KField("C", base=R, deg=2)
F2 = KField("F2")
F2_t = KField("F2(t)", base=F2, deg=float('inf'))
F2_t_sqrt = KField("F2(t)(sqrt(t))", base=F2_t, deg=2)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        K, L, M = witness
    except Exception:
        return [False, False, False]
    
    # H_1: K, L, and M are fields such that K is a subfield of L and L is a subfield of M
    try:
        if not (isinstance(K, KField) and isinstance(L, KField) and isinstance(M, KField)):
            h1 = False
        else:
            h1 = bool(K.is_subfield(L) and L.is_subfield(M))
    except Exception:
        h1 = False

    # H_2: The field extension M/L is finite
    try:
        if isinstance(M, KField) and isinstance(L, KField):
            h2 = bool(M.degree_over(L) < float('inf'))
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The conclusion FAILS.
    # Conclusion: M/K is finite, and deg(M/K) = deg(M/L)*deg(L/K)
    try:
        if isinstance(K, KField) and isinstance(L, KField) and isinstance(M, KField):
            deg_M_K = M.degree_over(K)
            deg_M_L = M.degree_over(L)
            deg_L_K = L.degree_over(K)
            
            is_finite = (deg_M_K < float('inf'))
            eq_holds = (deg_M_K == deg_M_L * deg_L_K)
            
            conclusion = is_finite and eq_holds
            neg_q = not conclusion
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K, L, M are fields such that K is a subfield of L and L is a subfield of M",
    "H_2: The field extension M/L is finite",
    "¬Q: M/K is infinite or deg(M/K) != deg(M/L)*deg(L/K)"
]

N_HYP = 2
NEG_Q_INDEX = 2