import sympy
from sympy.combinatorics import free_group

# Top-level setup: define a free group and some generators for the witness to use
F, x, y, z = free_group("x y z")

def conditions(witness):
    try:
        # The witness can be (u, v) or (F, X, u, v). We extract the last two elements.
        if not isinstance(witness, (tuple, list)) or len(witness) < 2:
            return [False, False, False]
            
        u, v = witness[-2], witness[-1]
        
        # H_1: F is a free group with a specified free basis X, and u, v are words in F
        # We verify that u and v are FreeGroupElements from the same free group.
        h1 = (type(u) is type(F.identity) and 
              type(v) is type(F.identity) and 
              u.group == v.group)
              
        if not h1:
            return [False, False, False]
            
        # Helper to expand the word into a flat tuple of (generator, sign) pairs
        def get_letters(w):
            letters = []
            for gen, exp in w.array_form:
                if exp > 0:
                    letters.extend([(gen, 1)] * exp)
                else:
                    letters.extend([(gen, -1)] * (-exp))
            return tuple(letters)
            
        # H_2: u and v are cyclically reduced words
        # FreeGroupElements are always reduced internally, so we only need to check 
        # if the first and last letters are inverses of each other.
        def is_cyclically_reduced(w):
            l = get_letters(w)
            if len(l) <= 1:
                return True
            if l[0][0] == l[-1][0] and l[0][1] == -l[-1][1]:
                return False
            return True
            
        h2 = is_cyclically_reduced(u) and is_cyclically_reduced(v)
        
        # ¬Q: u is NOT a cyclic permutation of v
        def is_cyclic_permutation(w1, w2):
            l1 = get_letters(w1)
            l2 = get_letters(w2)
            if len(l1) != len(l2):
                return False
            if len(l1) == 0:
                return True
            return any(l1 == l2[i:] + l2[:i] for i in range(len(l2)))
            
        neg_q = not is_cyclic_permutation(u, v)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a free group with a specified free basis X, and u, v are words in F",
    "H_2: u and v are cyclically reduced words",
    "¬Q: u is not a cyclic permutation of v"
]

N_HYP = 2
NEG_Q_INDEX = 2