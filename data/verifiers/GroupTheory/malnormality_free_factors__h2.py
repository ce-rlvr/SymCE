import sympy
from sympy.combinatorics.free_groups import FreeGroup, FreeGroupElement

# Top-level setup
# The witness is expected to be a tuple: (F, u, g, m, n)
# where F is a FreeGroup, u and g are FreeGroupElements in F.
# This implicitly defines the subgroup H = <u>.
# m and n are non-zero integers witnessing that u**m = g * u**n * g**-1,
# which proves that the intersection H \cap gHg^{-1} contains a non-trivial element.

def conditions(witness):
    try:
        F, u, g, m, n = witness
    except Exception:
        return [False, False, False]
    
    # H_1: F is a free group
    try:
        h1 = isinstance(F, FreeGroup)
    except Exception:
        h1 = False
        
    # H_2: g is an element of F such that g is not in H
    try:
        if not h1:
            h2 = False
        elif isinstance(g, FreeGroupElement) and isinstance(u, FreeGroupElement) and g in F and u in F:
            if u == F.identity:
                # If H is trivial, g not in H means g is not the identity
                h2 = (g != F.identity)
            else:
                # Check if g is a power of u. 
                # In a free group, the length of u**k is at least |k| for any non-trivial u.
                # Thus, we only need to check powers up to len(g).
                h2 = True
                max_k = len(g) + 1
                for k in range(-max_k, max_k + 1):
                    if u**k == g:
                        h2 = False
                        break
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The intersection H \cap gHg^{-1} is not the trivial subgroup
    try:
        if not h1:
            neg_q = False
        elif isinstance(g, FreeGroupElement) and isinstance(u, FreeGroupElement) and g in F and u in F:
            # We require m and n to be non-zero so that we are checking non-trivial powers.
            # We also ensure u**m is not the identity (which is guaranteed if u != 1 and m != 0 in a free group).
            if m != 0 and n != 0 and u**m != F.identity:
                neg_q = (u**m == g * (u**n) * (g**-1))
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: g is an element of F such that g is not in H",
    "¬Q: The intersection H \\cap gHg^{-1} is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2