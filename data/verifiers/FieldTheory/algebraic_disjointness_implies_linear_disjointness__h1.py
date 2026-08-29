import sympy
from sympy.polys.numberfields import primitive_element
from sympy import degree, S, I, sqrt
from sympy.abc import x

# Top-level setup
# Provide common algebraic numbers that might be used in a witness
omega = -S(1)/2 + sqrt(3)*I/2
cbrt2 = 2**(S(1)/3)

def conditions(witness):
    """
    Witness is expected to be a tuple of 4 lists of SymPy expressions:
    (K_gens, E_gens, F_gens, L_gens)
    representing the generators of the fields K, E, F, L over QQ.
    """
    try:
        K_gens, E_gens, F_gens, L_gens = witness
    except Exception:
        return [False, False, False, False]

    def deg(gens):
        """Computes the degree of the extension QQ(gens) over QQ."""
        if not gens:
            return 1
        filtered = []
        for g in gens:
            if isinstance(g, (int, float)):
                continue
            if getattr(g, 'is_Rational', False):
                continue
            filtered.append(g)
        if not filtered:
            return 1
        poly, _ = primitive_element(filtered, x)
        return degree(poly, x)

    # Precompute base degrees; if any fail, the witness is invalid (e.g., not algebraic)
    try:
        deg_K = deg(K_gens)
        deg_E = deg(E_gens)
        deg_F = deg(F_gens)
        deg_L = deg(L_gens)
    except Exception:
        return [False, False, False, False]

    try:
        # H_1: L is a field extension of K
        # True if L(K) has the same degree over QQ as L
        deg_LK = deg(L_gens + K_gens)
        h1 = (deg_LK == deg_L)
    except Exception:
        h1 = False

    try:
        # H_2: E and F are subfields of L that contain K
        deg_EK = deg(E_gens + K_gens)
        deg_FK = deg(F_gens + K_gens)
        deg_LE = deg(L_gens + E_gens)
        deg_LF = deg(L_gens + F_gens)
        h2 = (deg_EK == deg_E) and (deg_FK == deg_F) and (deg_LE == deg_L) and (deg_LF == deg_L)
    except Exception:
        h2 = False

    try:
        # H_3: E and F are algebraically disjoint over K
        # Since we restrict to algebraic extensions over QQ (verified by deg() succeeding),
        # the transcendence degree is 0. Any two algebraic extensions are algebraically disjoint.
        h3 = True
    except Exception:
        h3 = False

    try:
        # ¬Q: E and F are NOT linearly disjoint over K
        # E and F are linearly disjoint over K iff [EF : K] == [E : K] * [F : K]
        # which is equivalent to [EF : QQ] * [K : QQ] == [E : QQ] * [F : QQ]
        deg_EF = deg(E_gens + F_gens)
        linearly_disjoint = (deg_EF * deg_K == deg_E * deg_F)
        neg_q = not linearly_disjoint
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: L is a field extension of K",
    "H_2: E and F are subfields of L that contain K",
    "H_3: E and F are algebraically disjoint over K",
    "¬Q: E and F are not linearly disjoint over K"
]

N_HYP = 3
NEG_Q_INDEX = 3