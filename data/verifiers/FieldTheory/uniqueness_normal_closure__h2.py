import sympy
from sympy.polys.numberfields import field_isomorphism
from sympy.abc import x

# Top-level setup
# The witness should be a tuple, list, or dict providing the primitive elements 
# for the fields F, E, K1, K2 over Q.
# For example, to represent F=Q, E=Q(sqrt(2)), K1=Q(sqrt(2), sqrt(3)), K2=Q(sqrt(2), sqrt(5)):
# witness = (1, sympy.sqrt(2), sympy.sqrt(2) + sympy.sqrt(3), sympy.sqrt(2) + sympy.sqrt(5))

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness['F']
            e = witness['E']
            k1 = witness['K1']
            k2 = witness['K2']
        else:
            f, e, k1, k2 = witness
    except Exception:
        return [False, False]

    # H_1: E/F is an algebraic field extension
    # We verify this by checking if F is a subfield of E. 
    # Since they are represented by algebraic numbers, the extension is inherently algebraic.
    try:
        h1 = (field_isomorphism(f, e) is not None)
    except Exception:
        h1 = False

    # neg_Q: There is NO F-isomorphism from K1 to K2 that restricts to the identity map on E
    try:
        # For the restriction to the identity on E to even make sense, 
        # E must be a subfield of both K1 and K2.
        e_in_k1 = (field_isomorphism(e, k1) is not None)
        e_in_k2 = (field_isomorphism(e, k2) is not None)

        if not (e_in_k1 and e_in_k2):
            # If E is not a subfield, we conservatively return False to force 
            # the searcher to provide a well-posed counterexample.
            neg_q = False
        else:
            # If K1 and K2 are not Q-isomorphic, they cannot be F-isomorphic.
            deg_k1 = sympy.degree(sympy.minimal_polynomial(k1, x), x)
            deg_k2 = sympy.degree(sympy.minimal_polynomial(k2, x), x)

            if deg_k1 != deg_k2:
                neg_q = True
            else:
                iso = field_isomorphism(k1, k2)
                if iso is None:
                    neg_q = True
                else:
                    # They are Q-isomorphic. We conservatively return False
                    # to force the searcher to provide non-isomorphic fields,
                    # which guarantees the non-existence of the required F-isomorphism.
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is an algebraic field extension",
    "¬Q: There is no F-isomorphism from K_1 to K_2 that restricts to the identity map on E"
]

N_HYP = 1
NEG_Q_INDEX = 1