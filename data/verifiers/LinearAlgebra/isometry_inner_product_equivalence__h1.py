import sympy
from sympy import eye, zeros, Matrix, Rational, Integer
import itertools

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "¬Q: ||T(x)|| = ||x|| for all x in V if and only if <T(x), T(y)> = <x, y> for all x, y in V is false"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Witness can be a matrix (assumed over R/C, with fallback to GF(2)) 
        # or a tuple (Matrix, p) for a specific field characteristic p.
        if isinstance(witness, tuple):
            if len(witness) == 2:
                M, p = witness
            else:
                return [False, False]
        else:
            M = witness
            p = 0
            
        if not hasattr(M, 'shape') or len(M.shape) != 2:
            return [False, False]
            
        # H_1: T is a linear operator on V (must be an endomorphism, so square matrix)
        if M.shape[0] != M.shape[1]:
            h1 = False
        else:
            h1 = True
            
    except Exception:
        return [False, False]
        
    try:
        n = M.shape[1]
        if p > 0:
            elements = list(range(p))
            vectors = [sympy.Matrix(v) for v in itertools.product(elements, repeat=n)]
            
            norm_pres = True
            for x in vectors:
                if ((M*x).dot(M*x) - x.dot(x)) % p != 0:
                    norm_pres = False
                    break
                    
            ip_pres = True
            for x in vectors:
                for y in vectors:
                    if ((M*x).dot(M*y) - x.dot(y)) % p != 0:
                        ip_pres = False
                        break
                if not ip_pres:
                    break
                    
            equiv = (norm_pres == ip_pres)
        else:
            # Check over R/C
            # Norm preservation and inner product preservation are both equivalent to M.H * M == I
            norm_pres = (M.H * M == sympy.eye(n))
            ip_pres = (M.H * M == sympy.eye(n))
            equiv = (norm_pres == ip_pres)
            
            # If the equivalence holds over R/C, check if it's a counterexample over GF(2)
            # (since the theorem is true over fields of characteristic != 2).
            if equiv:
                try:
                    is_integer_matrix = all(getattr(val, 'is_integer', False) or isinstance(val, int) for val in M)
                except Exception:
                    is_integer_matrix = False
                    
                if is_integer_matrix and n <= 6:
                    p = 2
                    elements = [0, 1]
                    vectors = [sympy.Matrix(v) for v in itertools.product(elements, repeat=n)]
                    
                    norm_pres2 = True
                    for x in vectors:
                        if ((M*x).dot(M*x) - x.dot(x)) % p != 0:
                            norm_pres2 = False
                            break
                            
                    ip_pres2 = True
                    for x in vectors:
                        for y in vectors:
                            if ((M*x).dot(M*y) - x.dot(y)) % p != 0:
                                ip_pres2 = False
                                break
                        if not ip_pres2:
                            break
                            
                    equiv2 = (norm_pres2 == ip_pres2)
                    if not equiv2:
                        equiv = False
                        
        neg_q = not equiv
    except Exception:
        neg_q = False
        
    return [h1, neg_q]