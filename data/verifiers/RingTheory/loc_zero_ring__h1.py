import sympy

# Top-level setup: named object bindings that the witness expression may reference.
I2 = sympy.eye(2)
O2 = sympy.zeros(2, 2)
I3 = sympy.eye(3)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "The localized ring S^{-1}R is the zero ring if and only if 0 \in S"
    
    The dropped hypothesis is that R is a commutative ring. 
    For non-commutative rings (like M_n(K)), universal localization S^{-1}R 
    can be the zero ring even if 0 is not in S (e.g., if S contains a singular matrix).
    """
    try:
        # The witness can be provided as a tuple (R, S) or just S.
        if isinstance(witness, tuple) and len(witness) == 2:
            _, S = witness
        else:
            S = witness
            
        if not isinstance(S, (list, set, tuple)):
            return [False, False]
            
        S = list(S)
        if not S:
            return [False, False]
            
        # We expect the witness to be a subset of a matrix ring M_n(K)
        if all(hasattr(M, 'is_Matrix') and M.is_Matrix for M in S):
            n = S[0].shape[0]
            if not all(M.shape == (n, n) for M in S):
                return [False, False]
                
            # H_1: S is a multiplicatively closed subset
            h1 = True
            for A in S:
                for B in S:
                    if (A * B) not in S:
                        h1 = False
                        break
                if not h1:
                    break
                    
            # Check if S^{-1}R is the zero ring.
            # For R = M_n(K), the universal localization S^{-1}R is the zero ring 
            # if and only if S contains a singular matrix.
            has_singular = False
            for M in S:
                if sympy.simplify(M.det()) == 0:
                    has_singular = True
                    break
                    
            O_n = sympy.zeros(n, n)
            has_zero = (O_n in S)
            
            is_zero_ring = has_singular
            
            # Conclusion: S^{-1}R is the zero ring iff 0 \in S
            conclusion = (is_zero_ring == has_zero)
            neg_q = not conclusion
            
            return [h1, neg_q]
        else:
            # If not matrices, we evaluate H1 but assume it's a commutative ring
            # where the conclusion is always true (so neg_q is False).
            h1 = True
            for A in S:
                for B in S:
                    if (A * B) not in S:
                        h1 = False
                        break
                if not h1:
                    break
            return [h1, False]
            
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "¬Q: The localized ring S^{-1}R is the zero ring if and only if 0 \\in S (fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1