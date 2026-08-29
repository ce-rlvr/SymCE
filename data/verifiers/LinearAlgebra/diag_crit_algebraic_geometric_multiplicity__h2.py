import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # H1: A is an n by n matrix over a field F (we use Q as the field)
        if not isinstance(witness, Matrix):
            return [False, False]
        if witness.shape[0] != witness.shape[1]:
            return [False, False]
        n = witness.shape[0]
        if n < 1:
            return [False, False]
            
        # Ensure all entries are rational so the matrix is strictly over Q
        for i in range(n):
            for j in range(n):
                if not getattr(witness[i, j], 'is_rational', False):
                    return [False, False]
        h1 = True
    except Exception:
        return [False, False]
        
    try:
        evs = witness.eigenvals()
        
        # Check if A is diagonalizable over Q
        # This is true iff the sum of geometric multiplicities of rational eigenvalues equals n
        q_evs = {k: v for k, v in evs.items() if getattr(k, 'is_rational', False)}
        geom_sum = 0
        for e in q_evs:
            geom_sum += n - (witness - e * eye(n)).rank()
        is_diag_F = (geom_sum == n)
        
        # Check if algebraic multiplicity equals geometric multiplicity for ALL eigenvalues (over the algebraic closure)
        alg_eq_geom = True
        for e, alg in evs.items():
            geom = n - (witness - e * eye(n)).rank()
            if alg != geom:
                alg_eq_geom = False
                break
                
        # The conclusion states: A is diagonalizable iff alg_mult == geom_mult for each eigenvalue.
        # The negation of the conclusion is that this equivalence does NOT hold.
        neg_q = (is_diag_F != alg_eq_geom)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix over Q",
    "¬Q: (A is diagonalizable over Q) is not equivalent to (alg_mult == geom_mult for all eigenvalues)"
]

N_HYP = 1
NEG_Q_INDEX = 1