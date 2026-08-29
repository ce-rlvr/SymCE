import sympy
from sympy.matrices import MatrixBase, eye, zeros, Matrix
from sympy import gcd
from itertools import combinations

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture:
    "If T: V -> W is an injective linear map, then T has a left inverse."
    
    For vector spaces over a field, this is true. The conjecture is false 
    for modules over a ring (e.g., Z-modules or Q[x]-modules). We interpret 
    the witness as a matrix representing the linear map over its natural domain.
    """
    
    # H_1: T: V -> W is a linear map (represented as a matrix)
    try:
        h1 = isinstance(witness, MatrixBase)
    except Exception:
        h1 = False

    # H_2: T is injective
    # Over an integral domain, a matrix is injective iff its nullspace over the field of fractions is trivial.
    try:
        h2 = h1 and (witness.nullspace() == [])
    except Exception:
        h2 = False

    # ¬Q: There does NOT exist a linear map S: W -> V such that S ∘ T = I_V
    # i.e., the matrix does not have a left inverse over its ring of entries.
    try:
        if not h1:
            neg_q = False
        else:
            m, n = witness.shape
            if m < n:
                # Cannot be injective, but if it were, it wouldn't have a left inverse
                neg_q = True
            else:
                # Determine the domain of the matrix entries
                all_int = all(hasattr(e, 'is_integer') and e.is_integer for e in witness)
                
                if all_int:
                    # Over Z, a matrix has a left inverse iff the gcd of its n x n minors is 1
                    minors = [witness[list(rows), :].det() for rows in combinations(range(m), n)]
                    if not minors:
                        neg_q = False
                    else:
                        g = minors[0]
                        for m_val in minors[1:]:
                            g = gcd(g, m_val)
                        neg_q = abs(g) != 1
                        
                elif getattr(witness, 'free_symbols', None):
                    # Over polynomials, a matrix has a left inverse iff the gcd of its n x n minors is a non-zero constant
                    minors = [witness[list(rows), :].det() for rows in combinations(range(m), n)]
                    if not minors:
                        neg_q = False
                    else:
                        g = minors[0]
                        for m_val in minors[1:]:
                            g = gcd(g, m_val)
                        neg_q = not (hasattr(g, 'is_constant') and g.is_constant() and g != 0)
                        
                else:
                    # Over a field (e.g., Q, R, C), an injective matrix always has a left inverse
                    neg_q = witness.nullspace() != []
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear map (represented as a matrix)",
    "H_2: T is injective",
    "¬Q: T does not have a left inverse over its domain"
]

N_HYP = 2
NEG_Q_INDEX = 2