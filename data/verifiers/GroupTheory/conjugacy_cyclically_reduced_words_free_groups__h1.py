import sympy
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.fp_groups import FpGroup

# Top-level setup for potential witness expressions
FG2 = FreeGroup('a, b')
FG3 = FreeGroup('a, b, c')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (F, u, v, w) where:
      - F is a group (e.g., an FpGroup)
      - u, v are FreeGroupElements representing words in F's generators
      - w is a FreeGroupElement representing the conjugating element in F
    """
    try:
        F, u, v, w = witness
    except Exception:
        return [False, False]
        
    try:
        # H1: u and v are cyclically reduced words in F
        if hasattr(F, 'free_group'):
            FG = F.free_group
        else:
            FG = F
            
        h1 = (u.group == FG) and u.is_cyclically_reduced and \
             (v.group == FG) and v.is_cyclically_reduced
    except Exception:
        h1 = False

    try:
        # neg_Q: u and v are conjugate in F, but u is NOT a cyclic permutation of v
        if hasattr(F, 'free_group'):
            FG = F.free_group
            u_F = F(u)
            v_F = F(v)
            w_F = F(w)
            are_conjugate = (w_F**-1 * u_F * w_F == v_F)
        else:
            FG = F
            are_conjugate = (w**-1 * u * w == v)
            
        if w.group != FG:
            neg_q = False
        else:
            lu = list(u)
            lv = list(v)
            are_cyclic = False
            
            if len(lu) == len(lv):
                if not lu:
                    are_cyclic = True
                else:
                    n = len(lu)
                    for i in range(n):
                        if lu == lv[i:] + lv[:i]:
                            are_cyclic = True
                            break
                            
            # The conclusion is: conjugate in F iff cyclic permutations.
            # It fails if they are conjugate but NOT cyclic permutations.
            # (If they are cyclic permutations, they are always conjugate, so the iff holds).
            if are_conjugate and not are_cyclic:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: u and v are cyclically reduced words in F",
    "¬Q: u and v are conjugate in F but not cyclic permutations of each other"
]

N_HYP = 1
NEG_Q_INDEX = 1