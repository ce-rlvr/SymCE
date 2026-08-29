import sympy
from sympy import Matrix, Rational, Integer
from sympy.abc import x, y, z, t, u, v, w

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (F, E, B1, B2) where:
      - F is a list/set of generators for the base field over Q.
      - E is a list/set of generators for the extension field over Q.
      - B1 is a list/set of elements forming a transcendence basis for E over F.
      - B2 is a list/set of elements (the unconstrained set in the false conclusion).
    Generators should be SymPy expressions.
    """
    try:
        F, E, B1, B2 = witness
    except Exception:
        return [False, False, False]
    
    def tr_deg(S):
        """
        Computes the transcendence degree of a set of expressions over Q
        by calculating the rank of their Jacobian matrix with respect to all free symbols.
        """
        S = list(S)
        if not S:
            return 0
        syms = list(set().union(*(getattr(expr, 'free_symbols', set()) for expr in S)))
        if not syms:
            return 0
        try:
            J = Matrix(S).jacobian(syms)
            return J.rank()
        except Exception:
            return 0

    # H_1: E is a field extension of F
    # We verify this by checking if the generators of F are included in the generators of E.
    try:
        h1 = set(F).issubset(set(E))
    except Exception:
        h1 = False

    # H_2: B_1 is a transcendence basis for E over F
    try:
        B1_set = set(B1)
        # B_1 must be a subset of E
        is_subset = B1_set.issubset(set(E))
        
        # B_1 must be algebraically independent over F
        # tr_deg(F U B_1) == tr_deg(F) + |B_1|
        indep = tr_deg(list(F) + list(B1_set)) == tr_deg(list(F)) + len(B1_set)
        
        # E must be algebraic over F(B_1)
        # tr_deg(F U B_1 U E) == tr_deg(F U B_1)
        spans = tr_deg(list(F) + list(B1_set) + list(E)) == tr_deg(list(F) + list(B1_set))
        
        h2 = is_subset and indep and spans
    except Exception:
        h2 = False

    # ¬Q: The sets B_1 and B_2 do NOT have the same cardinality
    try:
        neg_q = len(set(B1)) != len(set(B2))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E is a field extension of F",
    "H_2: B_1 is a transcendence basis for E over F",
    "¬Q: B_1 and B_2 do not have the same cardinality"
]

N_HYP = 2
NEG_Q_INDEX = 2