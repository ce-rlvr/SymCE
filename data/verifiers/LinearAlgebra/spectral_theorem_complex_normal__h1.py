import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If T is a linear operator on V, then V possesses an orthonormal basis 
    consisting of eigenvectors of T if and only if T is normal."
    (The dropped hypothesis is that V is a complex inner product space).
    """
    # H_1: T is a linear operator on V (represented here as a square matrix)
    try:
        h1 = isinstance(witness, Matrix) and witness.is_square
    except Exception:
        h1 = False

    # neg_Q: The equivalence "V possesses an orthonormal basis of eigenvectors iff T is normal" FAILS.
    try:
        if not h1:
            neg_q = False
        else:
            T = witness
            # T is normal if it commutes with its conjugate transpose
            is_normal = (T * T.H == T.H * T)
            
            # Determine if the operator is over R or C.
            # We assume it's over R if all entries are real.
            is_real = True
            for e in T:
                if e.has(sympy.I) or e.is_real is False:
                    is_real = False
                    break
            
            # Over R, T has an orthonormal basis of eigenvectors iff T is symmetric.
            # Over C, T has an orthonormal basis of eigenvectors iff T is normal.
            if is_real:
                has_ortho_basis = (T == T.T)
            else:
                has_ortho_basis = is_normal
                
            # The conclusion is the equivalence (has_ortho_basis <-> is_normal).
            # The negated conclusion is that this equivalence does NOT hold.
            neg_q = bool(has_ortho_basis != is_normal)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "¬Q: The equivalence (V possesses an orthonormal basis of eigenvectors of T iff T is normal) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1