import sympy
from sympy import Matrix, eye, zeros, Symbol

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, neg_Q_ok].
    """
    # H_1: Let M be a block upper triangular matrix over a field F with square diagonal blocks A and B
    h1_ok = False
    try:
        if isinstance(witness, dict):
            M = witness['M']
            A = witness['A']
            B = witness['B']
        else:
            M, A, B = witness
            
        if hasattr(M, 'as_explicit'): M = M.as_explicit()
        if hasattr(A, 'as_explicit'): A = A.as_explicit()
        if hasattr(B, 'as_explicit'): B = B.as_explicit()
        
        if A.is_square and B.is_square and M.is_square:
            n = A.shape[0]
            m = B.shape[0]
            N = M.shape[0]
            
            # Find all occurrences of A on the diagonal
            A_offsets = []
            for i in range(N - n + 1):
                if M[i:i+n, i:i+n] == A:
                    A_offsets.append(i)
                    
            # Find all occurrences of B on the diagonal
            B_offsets = []
            for j in range(N - m + 1):
                if M[j:j+m, j:j+m] == B:
                    B_offsets.append(j)
                    
            # Check if there is any valid non-overlapping arrangement of A and B
            # that forms a block upper triangular partition of M
            for i in A_offsets:
                for j in B_offsets:
                    if i + n <= j:
                        # A comes before B
                        part = [i, n, j - i - n, m, N - j - m]
                    elif j + m <= i:
                        # B comes before A
                        part = [j, m, i - j - m, n, N - i - n]
                    else:
                        # Overlapping blocks, invalid partition
                        continue
                        
                    # Remove zero-sized blocks
                    part = [p for p in part if p > 0]
                    
                    is_but = True
                    row_offset = 0
                    for p in part:
                        if row_offset + p < N:
                            # Check the submatrix strictly below the current diagonal block
                            below = M[row_offset + p : N, row_offset : row_offset + p]
                            if not all(sympy.expand(x) == 0 for x in below):
                                is_but = False
                                break
                        row_offset += p
                        
                    if is_but:
                        h1_ok = True
                        break
                if h1_ok:
                    break
    except Exception:
        h1_ok = False

    # neg_Q: The characteristic polynomial of M is NOT the product of p_A(x) and p_B(x)
    neg_q_ok = False
    try:
        if isinstance(witness, dict):
            M = witness['M']
            A = witness['A']
            B = witness['B']
        else:
            M, A, B = witness
            
        if hasattr(M, 'as_explicit'): M = M.as_explicit()
        if hasattr(A, 'as_explicit'): A = A.as_explicit()
        if hasattr(B, 'as_explicit'): B = B.as_explicit()
        
        x = Symbol('x')
        p_M = M.charpoly(x).as_expr()
        p_A = A.charpoly(x).as_expr()
        p_B = B.charpoly(x).as_expr()
        
        # Check if the polynomials are different
        diff = sympy.expand(p_M - p_A * p_B)
        neg_q_ok = (diff != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: M is a block upper triangular matrix with square diagonal blocks A and B",
    "¬Q: The characteristic polynomial of M is not the product of p_A(x) and p_B(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1