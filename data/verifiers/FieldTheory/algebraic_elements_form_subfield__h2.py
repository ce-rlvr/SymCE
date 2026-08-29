import sympy

# Top-level setup
QQ = sympy.polys.domains.QQ
ZZ = sympy.polys.domains.ZZ
RR = sympy.polys.domains.RR
CC = sympy.polys.domains.CC
FF = sympy.polys.domains.FF

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (L, K, A) representing the fields/sets.
    """
    try:
        L, K, A = witness
    except Exception:
        return [False, False]
    
    # H_1: L/K is a field extension
    try:
        l_is_field = getattr(L, 'is_Field', False)
        k_is_field = getattr(K, 'is_Field', False)
        if l_is_field and k_is_field:
            # K is a subfield of L if unifying them yields L
            h1 = (L.unify(K) == L)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # ¬Q: A is not a subfield of L that contains K
    try:
        a_is_field = getattr(A, 'is_Field', False)
        if not a_is_field:
            q = False
        else:
            # A is a subfield of L
            a_sub_l = (L.unify(A) == L)
            # A contains K (K is a subfield of A)
            k_sub_a = (A.unify(K) == A)
            q = a_sub_l and k_sub_a
    except Exception:
        q = False
        
    neg_q = not q
    
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: L/K is a field extension",
    "¬Q: A is not a subfield of L that contains K"
]

N_HYP = 1
NEG_Q_INDEX = 1