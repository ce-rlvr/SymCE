import math
from sympy import eye, zeros, oo

# Top-level setup for potential matrix witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    The theorem is true for finite-dimensional vector spaces, but fails for infinite-dimensional ones.
    Therefore, the witness can be provided as a tuple of dimensions: (rank1, nullity1, rank2, nullity2)
    representing the dimensions of the image and kernel of two projection operators.
    Alternatively, it accepts a pair of Sympy matrices (though no finite-dimensional matrix pair can falsify it).
    """
    # 1. Try to unpack as a tuple of 4 dimensions: (rank1, nullity1, rank2, nullity2)
    if isinstance(witness, (tuple, list)) and len(witness) == 4:
        try:
            r1, n1, r2, n2 = witness
            
            def is_valid(x):
                try:
                    return float(x) >= 0
                except Exception:
                    return False
                    
            if is_valid(r1) and is_valid(n1) and is_valid(r2) and is_valid(n2):
                # H1: P1 and P2 are projection operators on the same space V
                # The dimension of V is rank + nullity.
                dim1 = r1 + n1
                dim2 = r2 + n2
                h1 = (dim1 == dim2)
                
                # Conclusion: P1 and P2 are similar iff they have the same rank
                same_rank = (r1 == r2)
                # Two projection operators are similar iff they have the same rank AND the same nullity
                similar = (r1 == r2) and (n1 == n2)
                
                q = (similar == same_rank)
                
                return [bool(h1), not bool(q)]
        except Exception:
            pass

    # 2. Try to treat as a pair of Sympy matrices
    try:
        P1, P2 = witness
        
        # H1: P1 and P2 are projection operators on the same space V
        h1 = (P1.shape == P2.shape) and (P1.shape[0] == P1.shape[1]) and (P1**2 == P1) and (P2**2 == P2)
        
        # Conclusion: P1 and P2 are similar iff they have the same rank
        same_rank = (P1.rank() == P2.rank())
        similar = P1.is_similar(P2)
        
        q = (similar == same_rank)
        
        return [bool(h1), not bool(q)]
    except Exception:
        pass

    # If witness format is unrecognized or evaluation fails
    return [False, False]

CONDITION_LABELS = [
    "H_1: P_1 and P_2 are projection operators on V",
    "¬Q: It is NOT the case that P_1 and P_2 are similar if and only if they have the same rank"
]

N_HYP = 1
NEG_Q_INDEX = 1