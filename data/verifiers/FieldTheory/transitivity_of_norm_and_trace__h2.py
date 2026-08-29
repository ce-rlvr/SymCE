import sympy
from sympy import QQ, Symbol, sqrt, I

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        K, L, M = witness
    except Exception:
        return [False, False, False]

    def is_field(F):
        return getattr(F, 'is_Field', False)
    
    def is_subfield(F1, F2):
        if F1 == F2:
            return True
        try:
            return F1.unify(F2) == F2
        except Exception:
            return False

    def is_fin_ext(E, F):
        if E == F:
            return True
        if F == sympy.RR and E == sympy.CC:
            return True
        if getattr(E, 'is_AlgebraicField', False):
            if F == sympy.QQ:
                return True
            if getattr(F, 'is_AlgebraicField', False) and is_subfield(F, E):
                return True
        return False

    # H_1: K, L, and M are fields such that K is a subfield of L, and L is a subfield of M.
    try:
        h1 = is_field(K) and is_field(L) and is_field(M) and is_subfield(K, L) and is_subfield(L, M)
    except Exception:
        h1 = False

    # H_2: L is a finite extension of K.
    try:
        h2 = is_fin_ext(L, K)
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails.
    # The conclusion states that for every element \alpha \in M, the norm and trace formulas hold.
    # This is true if M is a finite extension of K. If M is an infinite extension of K, 
    # the field norm and trace are generally undefined, so the formulas fail.
    try:
        neg_q = not is_fin_ext(M, K)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K, L, and M are fields such that K is a subfield of L, and L is a subfield of M",
    "H_2: L is a finite extension of K",
    "¬Q: The norm and trace formulas fail (e.g., M is an infinite extension of K, making them undefined)"
]

N_HYP = 2
NEG_Q_INDEX = 2