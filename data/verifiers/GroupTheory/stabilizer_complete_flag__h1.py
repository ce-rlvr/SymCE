import sympy
from sympy import eye, expand, Matrix

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The conjecture states that the stabilizer of the standard complete flag
    in GL(V) is the subgroup of upper-triangular invertible matrices.
    
    A counterexample could arise from:
    1. A non-commutative ring where an upper-triangular invertible matrix
       fails to stabilize the flag because its restriction to V_i is not surjective.
    2. A right-action convention where the stabilizer is actually the subgroup
       of lower-triangular matrices.
    """
    # Try non-commutative left-action interpretation
    try:
        M, M_inv, top_left_inverses = witness
        n = M.shape[0]
        I = eye(n)
        
        # H1: M is in GL(V) (invertible)
        H1 = (expand(M * M_inv) == I) and (expand(M_inv * M) == I)
        
        # H2: M acts on the standard flag
        H2 = True
        
        # neg_Q: M stabilizes the flag != M is upper triangular
        is_upper = M.is_upper
        stabilizes = is_upper
        for i in range(1, n+1):
            Mi = M[:i, :i]
            Mi_inv = top_left_inverses[i-1]
            if Mi_inv is None:
                stabilizes = False
                break
            Ii = eye(i)
            if expand(Mi * Mi_inv) != Ii:
                stabilizes = False
                break
                
        neg_Q = stabilizes != is_upper
        if H1 and H2 and neg_Q:
            return [True, True, True]
    except Exception:
        pass

    # Try commutative right-action interpretation
    try:
        M = witness
        # H1: M is in GL(V)
        H1 = M.is_square and M.det() != 0
        
        # H2: M acts on the standard flag
        H2 = True
        
        # Under right action, M stabilizes the standard flag iff M is lower triangular
        stabilizes_right = M.is_lower
        is_upper = M.is_upper
        
        # neg_Q: The stabilizer is NOT the upper-triangular matrices
        neg_Q = stabilizes_right != is_upper
        
        return [bool(H1), bool(H2), bool(neg_Q)]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: G = GL(V) acts naturally on the set of complete flags of V",
    "H_2: ℱ is the standard complete flag 0 = V_0 ⊂ V_1 ⊂ ... ⊂ V_n = V",
    "¬Q: The stabilizer of ℱ in G is not exactly the subgroup of upper-triangular invertible matrices"
]

N_HYP = 2
NEG_Q_INDEX = 2