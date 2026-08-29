import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (A, B, lambda).
    """
    try:
        A, B, lam = witness
    except Exception:
        return [False, False]
    
    # H_1: Let \lambda be a non-zero complex number.
    try:
        lam_sym = sp.sympify(lam)
        h1 = bool(lam_sym.is_complex and not lam_sym.is_zero)
    except Exception:
        h1 = False

    # Conclusion Q: The Jordan canonical form of AB and the Jordan canonical form of BA 
    # have exactly the same number of Jordan blocks of each size associated with the eigenvalue \lambda.
    try:
        AB = A * B
        BA = B * A
        
        def get_jordan_blocks(M, eigenvalue):
            # M.jordan_form() returns (P, J) where M = P * J * P^-1
            P, J = M.jordan_form()
            blocks = []
            n = J.shape[0]
            i = 0
            while i < n:
                val = J[i, i]
                size = 1
                # A Jordan block has the eigenvalue on the diagonal and 1s on the superdiagonal
                while i + size < n and J[i + size - 1, i + size] == 1 and (J[i + size, i + size] - val).is_zero:
                    size += 1
                
                # Check if this block is associated with the target eigenvalue
                if val == eigenvalue or (val - eigenvalue).is_zero:
                    blocks.append(size)
                i += size
            return sorted(blocks)
        
        blocks_AB = get_jordan_blocks(AB, lam_sym)
        blocks_BA = get_jordan_blocks(BA, lam_sym)
        
        q = (blocks_AB == blocks_BA)
    except Exception:
        # If AB or BA is not defined, not square, or doesn't have a Jordan form,
        # the statement about their Jordan canonical forms is false.
        q = False

    neg_q = not q

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: lambda is a non-zero complex number",
    "not Q: The Jordan canonical form of AB and BA do not have exactly the same number of Jordan blocks of each size associated with lambda"
]

N_HYP = 1
NEG_Q_INDEX = 1