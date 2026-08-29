import sympy
from sympy import minpoly, primitive_element, QQ
from sympy.abc import x, y, z

# Top-level setup
# (No specific named objects required for this field theory conjecture,
# but we provide standard symbols just in case)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    "If L is a separable algebraic extension of K, and L, M are subfields 
    of a common field extension of K, then L and M are linearly disjoint over K."
    
    The witness is expected to be a tuple of lists of generators for K, L, and M 
    over QQ. For example: ([], [sqrt(2)], [sqrt(2)]) for K=QQ, L=QQ(sqrt(2)), M=QQ(sqrt(2)).
    If a 2-tuple is provided, K is assumed to be QQ.
    """
    try:
        def to_list(val):
            if isinstance(val, (list, tuple, set)):
                return list(val)
            return [val]
            
        if len(witness) == 3:
            K_gens, L_gens, M_gens = map(to_list, witness)
        elif len(witness) == 2:
            K_gens = []
            L_gens, M_gens = map(to_list, witness)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def is_algebraic(gens):
        try:
            for g in gens:
                # minpoly will raise an exception if g is not algebraic over QQ
                minpoly(g)
            return True
        except Exception:
            return False

    # H_1: L and M are subfields of a common field extension of K
    # If all generators are algebraic over QQ, they embed into the algebraic closure of QQ,
    # which is a common field extension.
    try:
        h1 = is_algebraic(K_gens) and is_algebraic(L_gens) and is_algebraic(M_gens)
    except Exception:
        h1 = False

    # H_2: L is a separable algebraic extension of K
    # In characteristic 0 (QQ), all algebraic extensions are separable.
    try:
        h2 = h1 and is_algebraic(L_gens)
    except Exception:
        h2 = False

    # ¬Q: L and M are not linearly disjoint over K
    try:
        def get_deg(gens):
            unique_gens = []
            for g in gens:
                if g not in unique_gens and not g.is_Rational:
                    unique_gens.append(g)
            if not unique_gens:
                return 1
            if len(unique_gens) == 1:
                return minpoly(unique_gens[0]).degree()
            _, mp = primitive_element(unique_gens, domain=QQ)
            return mp.degree()

        # Compute degrees of the extensions over QQ
        deg_K = get_deg(K_gens)
        deg_L = get_deg(K_gens + L_gens)
        deg_M = get_deg(K_gens + M_gens)
        deg_LM = get_deg(K_gens + L_gens + M_gens)

        # L and M are linearly disjoint over K iff [L M : K] == [L : K] * [M : K]
        # Since these are finite extensions, we check if [L M : K] < [L : K] * [M : K]
        # Equivalently: deg_LM / deg_K < (deg_L / deg_K) * (deg_M / deg_K)
        # Which simplifies to: deg_LM * deg_K < deg_L * deg_M
        neg_q = (deg_LM * deg_K < deg_L * deg_M)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L and M are subfields of a common field extension of K",
    "H_2: L is a separable algebraic extension of K",
    "¬Q: L and M are not linearly disjoint over K"
]

N_HYP = 2
NEG_Q_INDEX = 2